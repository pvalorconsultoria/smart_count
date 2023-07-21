from abc import abstractmethod

from src.frame import Frame
from src.tasks.task import AbstractTask

from src.models.object_counting.v1.detection import Detection

class GetDetectionsTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

    def run(self, frame: Frame = None) -> Frame:
        frame["detections"] = dict()

        for obj in self.job.config.get_objects():
            frame["detections"][obj.NAME] = [
                Detection(frame.current_frame, contour, obj) 
                for contour in frame["contours"][obj.NAME]
            ]

        return frame
