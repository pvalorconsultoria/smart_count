from dataclasses import dataclass
from typing import Any, List

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from src.config import Config
from src.contour import Contour
from src.recognized_object import RecognizedObject
from src.config import ObjectConfig

class DetectionValidator:
    """Validates detections using a trained model."""

    def __init__(self, config) -> None:
        self.config = config
        self.model = load_model(self.config.TF_MODEL_PATH)

    def validate(self, detections: List['Detection'], frame: np.array) -> List[RecognizedObject]:
        """Validate the detections and classify them using the model."""
        clips = [
            cv2.cvtColor(clip.image, cv2.COLOR_BGR2GRAY)
            for detection in detections for clip in detection.clips
        ]
        clips = np.array(clips)[..., np.newaxis] if clips else np.array([])
        
        predictions = self.model.predict(clips) if clips.size > 0 else []

        recognized_objects = []
        idx = 0
        for detection in detections:
            for clip in detection.clips:
                if len(predictions) > 0 and predictions[idx][0] >= self.config.DETECTION_THRESHOLD:
                    recognized_objects.append(RecognizedObject(frame, clip, detection, predictions[idx][0], self.config))
                idx += 1

        return recognized_objects


class ImageClip:
    """Represents an image clip."""

    def __init__(self, x: int, y: int, image: Any, object_config: ObjectConfig):
        """
        Constructor to initialize the image clip.

        Parameters:
        x (int): The x-coordinate of the clip.
        y (int): The y-coordinate of the clip.
        image (Any): The image data of the clip.
        """
        self.config = object_config
        self.x = x
        self.y = y
        self.image = image

    def get_bounding_coords(self) -> tuple:
        """
        Get bounding coordinates of the clip.

        Returns:
        tuple: The bounding coordinates (x1, y1, x2, y2).
        """
        return self.x, self.y, self.x + self.config.CLIP_WIDTH, self.y + self.config.CLIP_HEIGHT

class Detection:
    """
    Represents a detected object.
    """

    def __init__(self, frame: np.ndarray, contour: Contour, config: ObjectConfig):
        """
        Initializes a Detection instance.

        Parameters:
        frame (np.ndarray): The frame where the object was detected.
        contour (Contour): The contour of the detected object.
        """
        self.config = config
        self.frame = frame
        self.contour = contour
        self.clips = self._clip_image()

    def _get_anchor_points(self) -> tuple:
        """
        Get anchor points for the detection.

        Returns:
        tuple: The anchor points (left, top), (right, top).
        """
        x, y, w, h = self.contour.get_bounding_box().get_coordinates()
        left = x
        right = x - w
        top = y

        return (left, top), (right, top)

    def _clip_image(self) -> list[ImageClip]:
        """
        Clip the image into segments.

        Returns:
        list[ImageClip]: The list of clipped image segments.
        """
        (left_anchor, top_anchor), (right_anchor, top_anchor) = self._get_anchor_points()

        clip_left = self.frame[top_anchor : top_anchor + self.config.CLIP_HEIGHT, left_anchor : left_anchor + self.config.CLIP_WIDTH, :]
        clip_right = self.frame[top_anchor : top_anchor + self.config.CLIP_HEIGHT, right_anchor : right_anchor + self.config.CLIP_WIDTH, :]

        clips = []
        if clip_left.shape == (self.config.CLIP_HEIGHT, self.config.CLIP_WIDTH, 3):
            clips.append(ImageClip(left_anchor, top_anchor, clip_left, self.config))
        if clip_right.shape == (self.config.CLIP_HEIGHT, self.config.CLIP_WIDTH, 3):
            clips.append(ImageClip(right_anchor, top_anchor, clip_right, self.config))

        return clips
