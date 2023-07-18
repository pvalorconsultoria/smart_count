from src.config import Config
from src.job import Job

class App:
    def __init__(self):
        self.current_job = None

    def start_job(self, video_path: str or int, config_file: str):
        self.current_job = Job(video_path, config_file)
        self.current_job.run()

        return self.current_job

    def process(self):
        return self.current_job.run()

    def is_running(self):
        if not self.current_job:
            return False
        
        return self.current_job.is_running()
    
    def get_current_frame(self):
        return self.current_job.video_pipeline.get_current_frame()