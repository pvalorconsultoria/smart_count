from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep
from typing import Union
import logging
import cv2
from rx import Observable
from src.config import Config

logging.basicConfig(level=logging.INFO)

class App:
    """Main application class for video processing."""

    def __init__(self):
        self.current_job = None

    def start_job(self, video_path: Union[str, int], config_file: str):
        """Start a new job for video processing."""
        self.current_job = LocalExecutionJob(video_path, config_file)
        self.current_job.start()

    # Placeholder methods. Consider implementing or removing them
    def process(self):
        pass

    def is_running(self):
        pass

    def get_current_frame(self):
        pass


class AbstractJob(ABC):
    """Abstract class for video processing jobs."""

    def __init__(self, video_path: Union[str, int], config_file: str):
        self.video_path = video_path
        self.config = Config(config_file)

    @abstractmethod
    def start(self):
        """Abstract method to start the job."""
        pass


class LocalExecutionJob(AbstractJob):
    """Local execution for video processing."""

    def __init__(self, video_path: Union[str, int], config_file: str):
        super().__init__(video_path, config_file)
        self.video_reader = VideoReaderStream(self)
        self.video_processor = VideoProcessor(self)
        self.video_local_viewer = VideoLocalViewer(self)

    def start(self):
        """Start processing the video."""
        self.video_reader_stream = self.video_reader.get_stream()
        self.video_result_stream = self.video_processor.get_stream()

        self.video_reader_stream.subscribe(
            on_next=self.video_processor.process_frame,
            on_error=self.video_processor.stop,
            on_completed=self.video_processor.stop
        )

        self.video_result_stream.subscribe(
            on_next=self.video_local_viewer.process_frame,
            on_error=self.video_local_viewer.stop,
            on_completed=self.video_local_viewer.stop
        )


class Frame:
    """Data structure to hold video frames and their timestamp."""

    def __init__(self, current_frame, next_frame):
        self.timestamp = datetime.now()
        self.current_frame = current_frame
        self.next_frame = next_frame

class VideoLocalViewer:

    def __init__(self, job: AbstractJob):
        self.job = job
        self.config = self.job.config

        cv2.namedWindow(self.config.FRAME_NAME)

    def process_frame(self, frame: Frame):
        logging.info("SHOW Frame")

        img = frame.current_frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imshow(self.config.FRAME_NAME, img)

    def stop(self):
        cv2.destroyAllWindows()


class VideoProcessor:
    """Class to process video frames."""

    def __init__(self, job: AbstractJob):
        self.job = job
        self.config = self.job.config
        self.is_processing = False
        self._stopped = False

    def process_frame(self, frame: Frame):
        """Process an individual frame."""
        logging.info("Received frame")
        self._execute_tasks(frame)

    def _execute_tasks(self, frame: Frame):
        self.result = frame.current_frame
        logging.info(f"Processed frame {frame.current_frame.shape}")

    def get_stream(self) -> Observable:
        """Get stream of processed results."""
        return Observable(self._emit_result)

    def _emit_result(self, observer, scheduler):
        """Emit processed results."""
        while not self._stopped:
            observer.on_next(self.result)
        observer.on_completed()

    def stop(self):
        """Stop processing."""
        self._stopped = True


class VideoReaderStream:
    """Class to read video frames and emit them as stream."""

    def __init__(self, job: AbstractJob):
        self.job = job
        self.video_path = self.job.video_path
        self.config = self.job.config
        self.video_finished = False
        self._init_video()

    def get_stream(self) -> Observable:
        """Get stream of video frames."""
        return Observable(self._emit_result)

    def _emit_result(self, observer, scheduler):
        """Emit frames as they are read."""
        while not self.video_finished and self.cap.isOpened():
            self._move_to_next_frame()
            observer.on_next(self.frame)
        observer.on_completed()

    def _init_video(self):
        """Initialize video source."""
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception("Error opening video source")
        _, current_frame = self.cap.read()
        _, next_frame = self.cap.read()
        self.frame = Frame(current_frame, next_frame)

    def _move_to_next_frame(self):
        """Skip and move to the desired frame."""
        for _ in range(self.config.FRAMES_TO_SKIP):
            if self.cap.isOpened():
                current_frame = self.frame.next_frame
                _, next_frame = self.cap.read()
                self.frame = Frame(current_frame, next_frame)
            else:
                self.video_finished = True
                break
