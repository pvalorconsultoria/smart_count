from typing import Union
from src.jobs.object_counting import ObjectCountingV1Job
from src.jobs.object_counting import ObjectCountingV2Job

class App:

    def __init__(self):
        self.current_job = None

    def start_job(self, video_path: Union[str, int], config_file: str):
        #self.current_job = ObjectCountingV1Job(video_path, config_file)
        self.current_job = ObjectCountingV2Job(video_path, config_file)

        self.current_job.start()

    def is_running(self):
        return self.current_job.is_running

    def get_current_frame(self):
        return self.current_job.result_frame

