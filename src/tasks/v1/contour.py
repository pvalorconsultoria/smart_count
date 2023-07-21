from abc import abstractmethod

from src.frame import Frame
from src.tasks.task import AbstractTask

from src.models.object_counting.v1.contour import get_contours_from_frames
from src.models.object_counting.v1.contour import filter_contours

class GetContoursTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)


    def run(self, frame: Frame = None) -> Frame:
        frame["contours"] = dict()

        contours = get_contours_from_frames(frame.current_frame, frame.next_frame)

        for obj in self.job.config.get_objects():
            filtered_contours = filter_contours(contours, obj.MIN_AREA, obj.MAX_AREA)

            frame["contours"][obj.NAME] = filtered_contours

        return frame
