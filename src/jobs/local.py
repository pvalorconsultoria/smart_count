from src.pipeline import Pipeline
from src.jobs import AbstractJob
from src.tasks.reader import VideoReaderTask
from src.tasks.local_viewer import VideoLocalViewerTask
from typing import Union

from src.tasks.v1.contour import GetContoursTask
from src.tasks.v1.detection import GetDetectionsTask
from src.tasks.v1.track import TrackAndValidateTask

class LocalExecutionJob(AbstractJob):

    def __init__(self, video_path: Union[str, int], config_file: str):
        super().__init__(video_path, config_file)

        self.pipeline = Pipeline([
            VideoReaderTask(self),
            GetContoursTask(self),
            GetDetectionsTask(self),
            TrackAndValidateTask(self),
            VideoLocalViewerTask(self)
        ])
