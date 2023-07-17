import cv2
import numpy as np

import unittest
from unittest.mock import Mock, patch
from src.object_counting.contour import Contour, get_contours_from_frames, filter_contours

class TestContour(unittest.TestCase):
    def setUp(self):
        self.mock_contour = Mock(spec=cv2.contourArea)
        self.contour = Contour(self.mock_contour)

    def test_contour_initialization(self):
        self.assertIsNotNone(self.contour.contour)
        self.assertIsNone(self.contour.bounding_box)

    def test_contour_get_area(self):
        with patch("cv2.contourArea", return_value=100):
            self.assertEqual(self.contour.get_area(), 100)

    def test_contour_draw(self):
        # Create a valid NumPy array as the frame input
        frame = np.zeros((100, 100, 3), dtype=np.uint8)

        with patch("cv2.drawContours"):
            self.contour.draw(frame)
            cv2.drawContours.assert_called_once()

    def test_contour_get_bounding_box(self):
        with patch("src.bounding_box.BoundingBox.from_contour"):
            bounding_box = self.contour.get_bounding_box()
            self.assertIsNotNone(bounding_box)
            self.assertIs(self.contour.get_bounding_box(), bounding_box)


class TestFunctions(unittest.TestCase):
    def test_get_contours_from_frames(self):
        # Create valid NumPy arrays as frame inputs
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)
        
        contours = get_contours_from_frames(frame1, frame2)
        self.assertEqual(len(contours), 0)

    def test_filter_contours(self):
        contour = Contour(Mock(spec=cv2.contourArea))
        contours = [contour] * 5  # A list of 5 identical contours
        with patch.object(Contour, "get_area", return_value=50):
            # Test filtering with a range that includes the contour area
            filtered = filter_contours(contours, min_area=20, max_area=100)
            self.assertEqual(len(filtered), 5)
            # Test filtering with a range that doesn't include the contour area
            filtered = filter_contours(contours, min_area=60, max_area=100)
            self.assertEqual(len(filtered), 0)

    def test_filter_contours_with_empty_list(self):
        contours = []
        filtered = filter_contours(contours, min_area=20, max_area=100)
        self.assertEqual(len(filtered), 0)

    def test_get_contours_from_frames_with_real_image(self):
        frame1 = np.zeros((100,100,3), dtype=np.uint8)
        frame2 = np.zeros((100,100,3), dtype=np.uint8)
        contours = get_contours_from_frames(frame1, frame2)
        self.assertEqual(len(contours), 0)  # No contours expected in two identical black frames

class TestContourEdgeCases(unittest.TestCase):
    def setUp(self):
        self.mock_contour = Mock(spec=cv2.contourArea)
        self.contour = Contour(self.mock_contour)

    def test_get_contours_from_frames_with_invalid_frames(self):
        invalid_frame = "this is not a valid frame"
        with self.assertRaises(ValueError):
            get_contours_from_frames(invalid_frame, invalid_frame)

    def test_get_bounding_box_twice(self):
        with patch("src.bounding_box.BoundingBox.from_contour") as mock_from_contour:
            bounding_box = self.contour.get_bounding_box()
            # If called again, the previous bounding box should be returned without calling from_contour again.
            bounding_box_2 = self.contour.get_bounding_box()
            mock_from_contour.assert_called_once()
            self.assertIs(bounding_box, bounding_box_2)
    
    def test_get_contours_from_frames_with_identical_frames(self):
        # If the frames are identical, there should be no contours
        frame1 = np.ones((100, 100, 3), np.uint8) * 255
        frame2 = frame1.copy()
        contours = get_contours_from_frames(frame1, frame2)
        self.assertEqual(len(contours), 0)

    def test_get_contours_from_frames_with_completely_different_frames(self):
        # If the frames are completely different, there should be contours
        frame1 = np.ones((100, 100, 3), np.uint8) * 255
        frame2 = np.zeros((100, 100, 3), np.uint8)
        contours = get_contours_from_frames(frame1, frame2)
        self.assertGreater(len(contours), 0)

class TestFunctionEdgeCases(unittest.TestCase):

    def test_get_contours_from_frames_with_none_frames(self):
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder frame
        frame2 = None  # Invalid frame
        with self.assertRaises(ValueError):
            get_contours_from_frames(frame1, frame2)

    def test_filter_contours_with_invalid_min_max_area(self):
        contour = Contour(Mock(spec=cv2.contourArea))
        contours = [contour]
        with self.assertRaises(ValueError):
            filter_contours(contours, min_area=100, max_area=50)  # min_area > max_area is invalid

    def test_filter_contours_with_none_contour(self):
        contours = [None]
        with self.assertRaises(AttributeError):
            filter_contours(contours, min_area=20, max_area=100)  # None contour should raise AttributeError

    def test_get_area_with_zero_area_contour(self):
        # Mocking cv2.contourArea inside the Contour class
        with patch("src.contour.cv2.contourArea", return_value=0):
            contour = Contour(None)  # Passing None to trigger the ValueError
            self.assertEqual(contour.get_area(), 0)

    def test_get_area_with_none_contour(self):
        # If for some reason the contour object is None, contourArea should raise an error
        with patch("cv2.contourArea", side_effect=TypeError):
            contour = Contour(None)
            with self.assertRaises(TypeError):
                contour.get_area()

if __name__ == '__main__':
    unittest.main()
