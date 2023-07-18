from src.config import Config
from src.video import VideoPipeline

class Job:
    def __init__(self, video_path: str or int, config_file: str):
        self.config = Config(config_file)
        self.video_pipeline = VideoPipeline(self.config, video_path)

    def run(self):
        self.video_pipeline.process()

    def is_running(self):
        return self.video_pipeline.is_running()