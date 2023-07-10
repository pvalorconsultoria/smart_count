import cv2

class BoundingBox:
    """
    A class used to represent a bounding box for contours in an image.
    """

    def __init__(self, reference, x=None, y=None, w=None, h=None):
        """
        Constructor to initialize the bounding box.
        :param reference: The contour reference.
        :param x: The x coordinate.
        :param y: The y coordinate.
        :param w: The width of the bounding box.
        :param h: The height of the bounding box.
        """
        self.ref = reference
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, frame):
        """
        Draw the bounding box on the frame.
        :param frame: The frame where the bounding box will be drawn.
        """
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)

    def get_coordinates(self):
        """
        Get the coordinates of the bounding box.
        :return: A tuple (x, y, w, h).
        """
        return self.x, self.y, self.w, self.h

    def get_bounding_coordinates(self):
        """
        Get the bounding coordinates of the bounding box.
        :return: A tuple (x1, y1, x2, y2).
        """
        return self.x, self.y, self.x + self.w, self.y + self.h

    @classmethod
    def from_contour(cls, contour):
        """
        Class method to create a BoundingBox object from a contour.
        :param contour: The contour used to create the bounding box.
        :return: A BoundingBox object.
        """
        (x, y, w, h) = cv2.boundingRect(contour)
        return cls(contour, x, y, w, h)
