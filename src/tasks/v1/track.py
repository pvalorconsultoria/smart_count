from abc import abstractmethod

from src.frame import Frame
from src.tasks.task import AbstractTask

from src.models.object_counting.v1.tracker import ObjectTracker
from src.models.object_counting.v1.detection import DetectionValidator

class TrackAndValidateTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self.validators = {obj.NAME: DetectionValidator(obj) for obj in self.job.config.get_objects()}
        self.trackers = {obj.NAME: ObjectTracker(obj) for obj in self.job.config.get_objects()}

    def run(self, frame: Frame = None) -> Frame:
        frame["recognized_objects"] = []
        
        for object_name, tracker in self.trackers.items():
            tracker.track(frame.current_frame)

            filtered_detections = tracker.filter_detections(frame["detections"][object_name])
            recognized_objects = self.validators[object_name].validate(filtered_detections, frame.current_frame)

            tracker.add(recognized_objects)

            frame["recognized_objects"].extend(recognized_objects)

        return frame
