import unittest
import numpy as np
from unittest.mock import Mock, patch

from src.config import ObjectConfig
from src.object_counting.v1.contour import Contour
from src.object_counting.v1.recognized_object import RecognizedObject
from src.config import ObjectConfig
from src.object_counting.v1.detection import Detection, DetectionValidator, ImageClip


class TestDetectionValidator(unittest.TestCase):

    def setUp(self):
        self.object_config = ObjectConfig(
            "object_name",
            "dataset_folder",
            100,
            200,
            50,
            50,
            0.5,
            0.7,
            "model_path",
            # Optional arguments can be skipped or provided if needed
        )

        self.detection_validator = DetectionValidator(self.object_config)

    def test_validate_with_empty_detections(self):
        # Arrange
        detections = []
        frame = np.zeros((100, 100, 3), dtype=np.uint8)

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_valid_detections(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.8]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], RecognizedObject)

    @patch('src.detection_validator.load_model')
    def test_validate_with_invalid_detections(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.4]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_empty_clips(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        detection.clips = []
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.8]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_empty_predictions(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_low_detection_threshold(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.3]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_multiple_detections(self, mock_load_model):
        # Arrange
        detection1 = Mock(spec=Detection)
        clip1 = Mock(spec=ImageClip)
        detection1.clips = [clip1]
        detection2 = Mock(spec=Detection)
        clip2 = Mock(spec=ImageClip)
        detection2.clips = [clip2]
        detections = [detection1, detection2]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.8], [0.2]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], RecognizedObject)

    @patch('src.detection_validator.load_model')
    def test_validate_with_invalid_model_output_shape(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([0.8])  # Invalid shape (1D instead of 2D)

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

    @patch('src.detection_validator.load_model')
    def test_validate_with_multiple_detections(self, mock_load_model):
        # Arrange
        detection1 = Mock(spec=Detection)
        clip1 = Mock(spec=ImageClip)
        detection1.clips = [clip1]
        detection2 = Mock(spec=Detection)
        clip2 = Mock(spec=ImageClip)
        detection2.clips = [clip2]
        detections = [detection1, detection2]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[0.8], [0.2]])

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], RecognizedObject)

    @patch('src.detection_validator.load_model')
    def test_validate_with_invalid_model_output_shape(self, mock_load_model):
        # Arrange
        detection = Mock(spec=Detection)
        clip = Mock(spec=ImageClip)
        detection.clips = [clip]
        detections = [detection]
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([0.8])  # Invalid shape (1D instead of 2D)

        # Act
        result = self.detection_validator.validate(detections, frame)

        # Assert
        self.assertEqual(len(result), 0)

class TestImageClip(unittest.TestCase):

    def setUp(self):
        self.object_config = ObjectConfig(
            "object_name",
            "dataset_folder",
            100,
            200,
            50,
            50,
            0.5,
            0.7,
            "model_path",
            # Optional arguments can be skipped or provided if needed
        )
        self.image_clip = ImageClip(0, 0, np.zeros((100, 100, 3), dtype=np.uint8), self.object_config)

    def test_get_bounding_coords(self):
        # Act
        result = self.image_clip.get_bounding_coords()

        # Assert
        self.assertEqual(result, (0, 0, self.object_config.CLIP_WIDTH, self.object_config.CLIP_HEIGHT))

    def test_init_with_invalid_image_dimensions(self):
        # Arrange
        image = np.zeros((100, 100, 2), dtype=np.uint8)  # Invalid height and width

        # Act and Assert
        with self.assertRaises(ValueError) as context:
            ImageClip(0, 0, image, self.object_config)

        self.assertEqual(str(context.exception), "Invalid image dimensions: expected (50, 50, 3), got (50, 50, 2)")


    def test_init_with_none_image(self):
        # Act and Assert
        with self.assertRaises(TypeError) as context:
            ImageClip(0, 0, None, self.object_config)

        self.assertEqual(str(context.exception), "Image argument cannot be None")

class TestDetection(unittest.TestCase):

    def setUp(self):
        self.object_config = ObjectConfig(
            "object_name",
            "dataset_folder",
            100,
            200,
            50,
            50,
            0.5,
            0.7,
            "model_path",
            # Optional arguments can be skipped or provided if needed
        )
        self.frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.contour = Mock(spec=Contour)
        self.detection = Detection(self.frame, self.contour, self.object_config)

    def test_get_anchor_points(self):
        # Arrange
        self.contour.get_bounding_box.return_value.get_coordinates.return_value = (10, 20, 30, 40)

        # Act
        result = self.detection._get_anchor_points()

        # Assert
        self.assertEqual(result, ((10, 20), (40, 20)))

    def test_clip_image_with_anchor_points_strategy(self):
        # Arrange
        self.object_config.CLIP_STRATEGY = 'ANCHOR_POINTS'
        self.detection._get_anchor_points.return_value = ((10, 20), (40, 20))
        self.frame[20:30, 10:20, :] = 255
        self.frame[20:30, 60:70, :] = 255

        # Act
        result = self.detection._clip_image()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ImageClip)
        self.assertIsInstance(result[1], ImageClip)

    def test_clip_image_with_default_strategy(self):
        # Arrange
        self.object_config.CLIP_STRATEGY = 'DEFAULT'
        self.contour.get_bounding_box.return_value.get_coordinates.return_value = (10, 20, 30, 40)
        self.frame[20:30, 10:20, :] = 255

        # Act
        result = self.detection._clip_image()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ImageClip)

    def test__clip_image_with_invalid_clip_dimensions(self):
        # Arrange
        self.object_config.CLIP_STRATEGY = 'ANCHOR_POINTS'
        self.detection._get_anchor_points.return_value = ((10, 20), (40, 20))
        self.frame[20:30, 10:19, :] = 255  # Invalid width (19 instead of 20)

        # Act
        result = self.detection._clip_image()

        # Assert
        self.assertEqual(len(result), 0)

    def test__clip_image_with_invalid_clip_dimensions(self):
        # Arrange
        self.object_config.CLIP_STRATEGY = 'ANCHOR_POINTS'
        self.detection._get_anchor_points.return_value = ((10, 20), (40, 20))
        self.frame[20:30, 10:19, :] = 255  # Invalid width (19 instead of 20)

        # Act
        result = self.detection._clip_image()

        # Assert
        self.assertEqual(len(result), 0)

    def test__clip_image_with_invalid_clip_dimensions(self):
        # Arrange
        self.object_config.CLIP_STRATEGY = 'ANCHOR_POINTS'
        self.detection._get_anchor_points.return_value = ((10, 20), (40, 20))
        self.frame[20:30, 10:19, :] = 255  # Invalid width (19 instead of 20)

        # Act
        result = self.detection._clip_image()

        # Assert
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
