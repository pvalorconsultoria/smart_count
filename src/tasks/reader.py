import cv2

from src.frame import Frame
from src.tasks import AbstractTask

class VideoReaderTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self.frame_number = 0
        self.video_finished = False

        self._init_video()

    def _init_video(self):
        self.cap = cv2.VideoCapture(self.job.video_path)
        if not self.cap.isOpened():
            raise Exception("Error opening video source")
        _, current_frame = self.cap.read()
        _, next_frame = self.cap.read()
        self.frame = Frame(current_frame, next_frame)
        self.frame["frame_number"] = self.frame_number + 1
        self.frame_number += 1

    def _move_to_next_frame(self):
        """Skip and move to the desired frame."""
        for _ in range(self.job.config.FRAMES_TO_SKIP):
            if self.cap.isOpened():
                current_frame = self.frame.next_frame
                _, next_frame = self.cap.read()
                self.frame = Frame(current_frame, next_frame)
                self.frame["frame_number"] = self.frame_number + 1
                self.frame_number += 1
            else:
                self.video_finished = True
                break    

    def run(self, frame: Frame = None) -> Frame:
        self._move_to_next_frame()
        return self.frame
