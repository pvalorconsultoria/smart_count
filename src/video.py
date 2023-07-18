import cv2
import time

from src.frame import Frame, FrameQueue
from src.thread import StoppableThread

class VideoReader:
    def __init__(self, config, video_path, read_queue, max_queue_size=10):
        self.config = config
        self.video_path = video_path
        self.read_queue = read_queue
        self.max_queue_size = max_queue_size
        self.video_finished = False
        self._init_video()

    def process(self):
        if not self.video_finished and self.cap.isOpened():
            self._move_to_next_frame()

            if self.read_queue.qsize() >= self.max_queue_size:
                self.read_queue.get_nowait()

            self.read_queue.put_nowait(self.frame)
        else:
            self.release()

    def release(self):
        self.cap.release()
        self.video_finished = True

    def _move_to_next_frame(self):
        for _ in range(self.config.FRAMES_TO_SKIP):
            if self.cap.isOpened():
                current_frame = self.frame.next_frame
                _, next_frame = self.cap.read()
                self.frame = Frame(current_frame, next_frame)
            else:
                break

    def _init_video(self):
        if isinstance(self.video_path, int):
            print(f'Initializing video capture from webcam {self.video_path}')
        else:
            print(f'Initializing video capture from video file {self.video_path}')
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception("Error opening video source")
        _, current_frame = self.cap.read()
        _, next_frame = self.cap.read()
        self.frame = Frame(current_frame, next_frame)

class VideoViewer:
    def __init__(self, config, read_queue):
        self.config = config
        self.read_queue = read_queue

    def process(self):
        frame = self.read_queue.get()
        self._draw_frame(frame)

    def _draw_frame(self, frame: Frame):
        cv2.imshow(self.config.FRAME_NAME, frame.current_frame)

    def release(self):
        cv2.destroyAllWindows()

class VideoProcessor():
    def __init__(self, config, read_queue, processed_queue):
        self.config = config
        self.read_queue = read_queue
        self.processed_queue = processed_queue
        self.is_processing = False
        self.result = None
        self.current_process = None
        self.current_frame = None

    def _process_frame(self, frame):
        print("Aqui 1")
        time.sleep(10)
        print("Aqui 2")
        self.result = True

    def _start_process(self):
        self.current_frame = self.read_queue.get_nowait()
        self.is_processing = True
        self.current_thread = StoppableThread(target=self._process_frame, args=(self.current_frame,))
        self.current_thread.start()

    def _end_process(self):
        self.is_processing = False
        self.current_thread.stop()

    def process(self):
        if not self.is_processing:
            if self.result:
                self.processed_queue.put_nowait(self.result)
                self._end_process()

            self._start_process()

class VideoPipeline:
    def __init__(self, config, video_path):
        self.config = config

        self.read_queue = FrameQueue()
        self.processed_queue = FrameQueue()

        self.video_reader = VideoReader(config, video_path, self.read_queue)
        self.video_processor = VideoProcessor(config, self.read_queue, self.processed_queue)
        self.pipeline_ended = False

        if self.config.DISPLAY_WINDOW:
            self.video_viewer = VideoViewer(config, self.read_queue)
            cv2.namedWindow(self.config.FRAME_NAME)

    def process(self):
        if not self.video_reader.video_finished:
            self.video_reader.process()
            self.video_processor.process()

            if self.config.DISPLAY_WINDOW:
                self.video_viewer.process()

                if cv2.waitKey(40) == 27:
                    self.video_reader.video_finished = True
        else:
            self.pipeline_ended = True
            if self.config.DISPLAY_WINDOW:
                self.video_viewer.release()

    def is_running(self):
        return not self.pipeline_ended

    def get_current_frame(self):
        return self.video_reader.frame.current_frame