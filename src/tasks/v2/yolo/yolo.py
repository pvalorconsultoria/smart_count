import cv2

from abc import abstractmethod

from transformers import YolosImageProcessor, YolosForObjectDetection
import torch

import threading

from src.frame import Frame
from src.tasks.task import AbstractTask

def corners_to_xywh(x0, y0, x1, y1):
    x = x0
    y = y0
    w = x1 - x0
    h = y1 - y0
    return x, y, w, h

class RunYoloModelTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self._model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self._image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

        self._is_processing = False
        self._current_predictions = None

        self._processing_thread = None

    def _process_frame(self, frame: Frame = None) -> None:
        self._is_processing = True

        image = frame.array()

        inputs = self._image_processor(images=image, return_tensors="pt")
        outputs = self._model(**inputs)

        target_sizes = torch.tensor([image.shape[:2]])
        results = self._image_processor.post_process_object_detection(outputs, threshold=0.8, target_sizes=target_sizes)[0]

        predictions = self._get_predictions(frame, results)

        self._current_predictions = predictions
        self._is_processing = False

    def _clip_box_from_frame(self, frame, bbox):
        x, y, w, h = bbox

        return frame.array()[y:y+h,x:x+w,:]

    def _get_predictions(self, frame: Frame, results):
        predictions = []
        
        for score, label, bbox in zip(results["scores"], results["labels"], results["boxes"]):
            bbox = [round(i) for i in bbox.tolist()]
            bbox = corners_to_xywh(*bbox)

            #clip = self._clip_box_from_frame(frame, bbox)

            predictions.append({
                "bbox": bbox,
                "score": round(score.item(), 3),
                "label": self._model.config.id2label[label.item()],
                "clip_frame": frame.array()
            })

        return predictions

    def run(self, frame: Frame = None) -> Frame:
        frame["yolo_predictions"] = None
        
        if self._is_processing:
            return frame

        if self._current_predictions:
            frame["yolo_predictions"] = self._current_predictions
            self._current_predictions = None
        else:
            self._processing_thread = threading.Thread(target=self._process_frame, args=(frame,))
            self._processing_thread.start()

        return frame


