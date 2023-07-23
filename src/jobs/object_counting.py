from typing import Union

from src.pipeline import Pipeline
from src.jobs import AbstractJob

from src.tasks.reader import VideoReaderTask
from src.tasks.local_viewer import VideoLocalViewerTask
from src.tasks.fps import FrameRateControlTask

from src.tasks.v1.contour import GetContoursTask
from src.tasks.v1.detection import GetDetectionsTask
from src.tasks.v1.track import TrackAndValidateTask
from src.tasks.v2.yolo import RunYoloModelTask
from src.tasks.v2.yolo import TrackYoloDetectionsTask
from src.tasks.v2.yolo import RunYoloV8ModelTask

class ObjectCountingV1Job(AbstractJob):

    def __init__(self, video_path: Union[str, int], config_file: str):
        super().__init__(video_path, config_file)

        self.pipeline = Pipeline([
            VideoReaderTask(self),
            GetContoursTask(self),
            GetDetectionsTask(self),
            TrackAndValidateTask(self),
            VideoLocalViewerTask(self)
        ])

class ObjectCountingV2Job(AbstractJob):

    def __init__(self, video_path: Union[str, int], config_file: str):
        super().__init__(video_path, config_file)

        self.pipeline = Pipeline([
            VideoReaderTask(self),
            RunYoloV8ModelTask(self),
            TrackYoloDetectionsTask(self),
            VideoLocalViewerTask(self),
            FrameRateControlTask(self)
        ])
