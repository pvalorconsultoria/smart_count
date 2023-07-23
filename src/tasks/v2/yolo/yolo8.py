import cv2
from dataclasses import dataclass
from typing import Any
import threading
from src.frame import Frame
from src.tasks.task import AbstractTask
from ultralytics import YOLO

@dataclass
class Prediction:
    """
    Data class to store prediction information.
    """
    bbox: Any  # List of (x, y, w, h) representing bounding box coordinates
    score: float  # Confidence score of the prediction
    label: str  # Label of the predicted object
    frame: Frame  # Input Frame object

@dataclass
class YoloPrediction:
    frame: Frame
    predictions: list[Prediction]

class YoloV8Model:
    """
    YOLOv8 model wrapper for object detection.
    """
    def __init__(self, model_path="yolov8n.pt"):
        """
        Initialize the YOLOv8 model.

        Args:
            model_path (str): Path to the YOLOv8 model checkpoint file.
        """
        self.model_path = model_path
        self._model = YOLO(model_path)
        self._target_labels = ["car"]

    def _corners_to_xywh(self, x0, y0, x1, y1):
        """
        Convert corner coordinates (x0, y0, x1, y1) to (x, y, w, h) format.

        Args:
            x0 (float): x-coordinate of the top-left corner.
            y0 (float): y-coordinate of the top-left corner.
            x1 (float): x-coordinate of the bottom-right corner.
            y1 (float): y-coordinate of the bottom-right corner.

        Returns:
            Tuple[float, float, float, float]: (x, y, w, h) format bounding box.
        """
        x = x0
        y = y0
        w = x1 - x0
        h = y1 - y0
        return x, y, w, h

    def _get_predictions(self, frames, results):
        """
        Process YOLOv8 results and generate Prediction objects.

        Args:
            frames (list[Frame]): List of Frame objects (input images).
            results: YOLOv8 detection results.

        Returns:
            list[YoloPrediction]: List of YoloPrediction objects.
        """
        yolo_predictions = []

        for frame, result in zip(frames, results):
            predictions = []
            
            for bbox, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                bbox = [round(i) for i in bbox.tolist()]
                bbox = self._corners_to_xywh(*bbox)

                label = result.names[cls.item()]

                if label in self._target_labels:
                    prediction = Prediction(
                        bbox=bbox,
                        score=round(conf.item(), 3),
                        label=label,
                        frame=frame
                    )

                    predictions.append(prediction)
            
            yolo_prediction = YoloPrediction(frame, predictions)
            yolo_predictions.append(yolo_prediction)

        return yolo_predictions

    def predict(self, frames):
        """
        Run object detection on input frames and generate predictions.

        Args:
            frames (list[Frame]): List of Frame objects (input images).

        Returns:
            list[Prediction]: List of Prediction objects.
        """
        images = [frame.array() for frame in frames]

        results = self._model.predict(images)

        predictions = self._get_predictions(frames, results)

        return predictions


class RunYoloV8ModelTask(AbstractTask):
    """
    Task to run YOLOv8 model for object detection on incoming frames.
    """
    def __init__(self, job):
        """
        Initialize the RunYoloV8ModelTask.

        Args:
            job: The job object (not clear from the provided code).
        """
        super().__init__(job)

        self._model = YoloV8Model()

        self._frames_window_size = 4
        self._current_frames = []

        self._starting_frame = None
        self._ending_frame = None

        self._is_processing = False
        self._current_predictions = None

        self._processing_thread = None

    def _process_frames(self):
        """
        Process the frames using the YOLOv8 model.
        """
        self._is_processing = True

        self._current_predictions = self._model.predict(self._current_frames)

        self._is_processing = False
        self._current_frames = []

    def run(self, frame=None):
        """
        Run the YOLOv8 model on the input frame.

        Args:
            frame (Frame): Input Frame object.

        Returns:
            Frame: Frame object with YOLO predictions (if available).
        """
        frame["yolo_predictions"] = None

        if self._is_processing:
            return frame

        if self._current_predictions:
            self._ending_frame = frame["frame_number"]

            frame["yolo_predictions"] = self._current_predictions
            frame["frame_number_delta"] = self._ending_frame - self._starting_frame

            self._current_predictions = None
        else:
            if len(self._current_frames) <= self._frames_window_size:
                self._current_frames.append(frame)
            else:
                self._starting_frame = frame["frame_number"]

                self._processing_thread = threading.Thread(target=self._process_frames)
                self._processing_thread.start()

        return frame
