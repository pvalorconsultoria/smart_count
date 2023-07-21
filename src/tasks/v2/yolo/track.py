import cv2

from src.frame import Frame
from src.tasks.task import AbstractTask

from src.models.object_counting.v1.detection import Detection

class TrackYoloDetectionsTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

    def _draw_predictions(self, predictions, frame):
        for prediction in predictions:
            cv2.rectangle(frame, prediction["box"], (0, 0, 255), 2)

    def run(self, frame: Frame = None) -> Frame:
        print(frame["yolo_predictions"])

        if frame["yolo_predictions"]:
            self._draw_predictions(frame["yolo_predictions"], frame.current_frame)

        return frame
