import os
import cv2
from src.config import Config
from src.object_counting.v1 import ObjectCounting

class App:
    """
    The main application class. This class is responsible for handling video input, 
    interacting with the user through the GUI, and delegating tasks to specialized components.
    """
    
    def __init__(self, video_source: str or int, config_file: str):
        """
        Constructor to initialize video file, tracking and detection, and video capture if needed.
        :param video_source: Path to the video file or index of the webcam.
        :param config_file: Path to the configuration file.
        """
        self.config = Config(config_file)
        self.object_counter = ObjectCounting(self.config)

        self._init_video(video_source)
        self.should_capture_video = False
        self._init_capture_if_needed()

        # Register the mouse event handler
        if self.config.DISPLAY_WINDOW:
            cv2.namedWindow(self.config.FRAME_NAME)
            cv2.setMouseCallback(self.config.FRAME_NAME, self.object_counter.handle_mouse_event)
    
    def _init_video(self, video_source: str or int):
        """
        Initializes video capture and reads the first two frames.
        """
        if isinstance(video_source, int):
            print(f'Initializing video capture from webcam {video_source}')
        else:
            print(f'Initializing video capture from video file {video_source}')

        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise Exception("Error opening video source")

        _, self.current_frame = self.cap.read()
        _, self.next_frame = self.cap.read()

    def _init_capture_if_needed(self):
        """
        Initializes video capture if capturing video is enabled.
        """
        if self.should_capture_video:
            video_h, video_w, _ = self.current_frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video = cv2.VideoWriter(self.config.OUTPUT_VIDEO_PATH, fourcc, 30, (video_w, video_h))
    
    def process_frame(self):
        """
        Main method to process a video frame - delegate the object counting tasks to the ObjectCounting instance
        and move on to the next frame.
        """
        recognized_objects = self.object_counter.process_frame(self.current_frame, self.next_frame)

        if self.config.DISPLAY_WINDOW:
            self._draw_frame(recognized_objects)

        self._capture_video()
        self._move_to_next_frame()

    def _draw_frame(self, recognized_objects):
        """
        Draws frame with logo, counter and (optionally) contours and recognized objects.
        """        
        cv2.imshow(self.config.FRAME_NAME, self.current_frame)

    def _capture_video(self):
        """
        Captures the current frame to the video file if capturing video is enabled.
        """
        if self.should_capture_video:
            self.video.write(self.current_frame)

    def _move_to_next_frame(self):
        """
        Moves on to the next frame by discarding the current frame and reading the next one.
        Skips a predefined number of frames in each iteration.
        """
        for _ in range(self.config.FRAMES_TO_SKIP):
            if self.cap.isOpened():
                self.current_frame = self.next_frame
                _, self.next_frame = self.cap.read()
            else:
                break

    def is_opened(self):
        """
        Check if video capture is properly opened.
        """
        return self.cap.isOpened()

    def release_resources(self):
        """
        Releases video and capture resources and closes windows.
        """
        if self.should_capture_video:
            self.video.release()

        cv2.destroyAllWindows()
        self.cap.release()
