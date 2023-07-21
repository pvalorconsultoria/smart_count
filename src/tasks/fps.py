import time
from src.frame import Frame
from src.tasks.task import AbstractTask

class FrameRateControlTask(AbstractTask):
    def __init__(self, job, fps=27):
        super().__init__(job)

        self._fps = fps
        self._frame_interval = 1.0 / fps
        self._last_processed_time = time.time()

    def run(self, frame: Frame = None) -> Frame:
        current_time = time.time()
        elapsed_time = current_time - self._last_processed_time

        if elapsed_time < self._frame_interval:
            # If the desired interval has not elapsed, sleep to maintain the frame rate
            time.sleep(self._frame_interval - elapsed_time)

        # Update the last processed time to the current time
        self._last_processed_time = time.time()

        # Return the original frame
        return frame
