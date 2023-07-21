from abc import ABC
from typing import Union

from src.config import Config
from src.pipeline import Pipeline

class AbstractJob(ABC):
    pipeline = Pipeline([])

    def __init__(self, video_path: Union[str, int], config_file: str):
        self.video_path = video_path
        self.config = Config(config_file)

        self.result_frame = None
        self.is_running = False

    def start(self):
        self.is_running = True
        self.run()

    def run(self):
        while self.is_running:
            self.result_frame = self.pipeline.run()

    def stop(self):
        self.is_running = False
        self.pipeline.release()


