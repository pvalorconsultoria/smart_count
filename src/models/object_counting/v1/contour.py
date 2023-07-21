import numpy as np
import cv2
from src.models.object_counting.v1.bounding_box import BoundingBox

class Contour:
    """
    A class used to represent a contour in an image.
    """

    def __init__(self, contour):
        """
        Constructor to initialize the contour.
        :param contour: The contour from the image.
        """
        self.contour = contour
        self.bounding_box = None

    def get_area(self):
        """
        Calculate the area of the contour.
        :return: The area of the contour.
        """
        try:
            return cv2.contourArea(self.contour)
        except cv2.error:
            raise ValueError("Invalid contour data. Expected numpy array.")

    def draw(self, frame):
        """
        Draw the contour on the frame.
        :param frame: The frame where the contour will be drawn.
        """
        if not isinstance(frame, np.ndarray):
            raise ValueError("Invalid frame. Frame must be a numpy array.")
        cv2.drawContours(frame, [self.contour], 0, (0, 255, 0), 2)
    
    def get_bounding_box(self):
        """
        Get the bounding box of the contour.
        :return: A BoundingBox object of the contour.
        """
        if not self.bounding_box:
            self.bounding_box = BoundingBox.from_contour(self.contour)

        return self.bounding_box

def get_contours_from_frames(frame1, frame2) -> list[Contour]:
    """
    Get contours from two image frames.
    
    :param frame1: The first image frame.
    :param frame2: The second image frame.
    :return: A list of Contour objects representing detected contours.
    """

    if not isinstance(frame1, np.ndarray) or not isinstance(frame2, np.ndarray):
        raise ValueError("Frames must be numpy arrays.")

    # Calculate the absolute difference between the two input frames.
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference image to grayscale.
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the grayscale image.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply a binary threshold to the blurred image.
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Apply dilation operation on the threshold image.
    dilated = cv2.dilate(thresh, None, iterations=1)

    # Find the contours in the dilated image.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return [Contour(contour) for contour in contours]

def filter_contours(contours, min_area, max_area):
    """
    Filter the contours based on their area.
    :param contours: The list of Contour objects.
    :param min_area: The minimum area for a contour to be included.
    :param max_area: The maximum area for a contour to be included.
    :return: The list of filtered Contour objects.
    """
    return [contour for contour in contours 
            if min_area < contour.get_area() < max_area]
