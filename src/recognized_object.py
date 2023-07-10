import numpy as np
import cv2

from src.config import ObjectConfig

class RecognizedObject:
    """
    Represents an object that was recognized in a video frame.
    """
    def __init__(self, frame, clip, detection, confidence, object_config: ObjectConfig):
        """
        Initializes a RecognizedObject instance.

        Parameters:
        frame (np.array): The frame where the object was recognized.
        clip (Clip): The clip of the recognized object.
        detection (Detection): The detection data of the recognized object.
        confidence (float): The confidence score of the detection.
        object_config (ObjectConfig): The Object Configuration
        """
        self.frame = frame
        self.clip = clip
        self.detection = detection
        self.confidence = confidence
        self.config = object_config

        self.count = None

        self.roi_hist = None

        self.track_piece = (self.clip.x, self.clip.y, self.config.CLIP_WIDTH, self.config.CLIP_HEIGHT)

        self.tracker = cv2.legacy.TrackerMedianFlow_create()
        self.tracker.init(frame, self.track_piece)

        self.lost_track = False

    def draw(self, frame):
        """
        Draws the bounding box and confidence score of the recognized object on the frame.

        Parameters:
        frame (np.array): The frame where to draw the bounding box and confidence score.
        """
        x, y, w, h = self.track_piece
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, f'{self.count} | {self.confidence:0.3f}', 
                    (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 0, 255), 2)

    def get_bounding_coords(self):
        """
        Gets the coordinates of the bounding box of the recognized object.

        Returns:
        tuple: The coordinates of the bounding box (x1, y1, x2, y2).
        """
        x, y, w, h = self.track_piece
        return x, y, x + w, y + h

    def track(self, frame):
        """
        Tracks the recognized object in a frame using the defined tracker.

        Parameters:
        frame (np.array): The frame where to track the recognized object.
        """
        _, track_box = self.tracker.update(frame)

        x, y, w, h = self.track_piece
        nx, ny = map(int, track_box[:2])

        if self.config.CONVEYOR_DIRECTION == 'RIGHT':
            x = max(x + self.config.CONVEYOR_SPEED, nx)
        elif self.config.CONVEYOR_DIRECTION == 'LEFT':
            x = min(x - self.config.CONVEYOR_SPEED, nx)
        elif self.config.CONVEYOR_DIRECTION == 'DOWN':
            y = max(y + self.config.CONVEYOR_SPEED, ny)
        elif self.config.CONVEYOR_DIRECTION == 'UP':
            y = min(y - self.config.CONVEYOR_SPEED, ny)

        # Update the position of the bounding box 
        self.track_piece = (x, y, w, h)

        # Check if bounding box has reached edge of frame
        frame_height, frame_width = frame.shape[:2]
        if any([coord <= 0 or coord >= dim for coord, dim in zip(self.track_piece[:2], [frame_width, frame_height])]):
            # Left or right edge, or top or bottom edge
            self.lost_track = True

        if not self.lost_track:
            self.draw(frame)
