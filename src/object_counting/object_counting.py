import os

import cv2

from src.object_counting.contour import filter_contours, get_contours_from_frames
from src.object_counting.detection import Detection, DetectionValidator
from src.object_counting.tracker import ObjectTracker

class ObjectCounting:
    """
    Class to encapsulate object detection and tracking in video frames. The class relies on predefined 
    configuration objects that specify the characteristics of the objects of interest, including their names 
    and the models used for their detection.

    Methods
    -------
    process_frame(current_frame, next_frame):
        Analyzes a pair of video frames to identify and track objects of interest.
    """

    def __init__(self, config):
        """
        Constructor that initializes detection validators and object trackers for each object in the configuration.
        
        Parameters
        ----------
        config : Config
            A configuration object that holds the settings and parameters for object detection and tracking.
        """
        self.config = config
        self.validators = {obj.NAME: DetectionValidator(obj) for obj in self.config.get_objects()}
        self.trackers = {obj.NAME: ObjectTracker(obj) for obj in self.config.get_objects()}

    def _get_object_config(self, object_name):
        """
        Retrieves the configuration for a specific object.
        
        Parameters
        ----------
        object_name : str
            The name of the object whose configuration is to be retrieved.

        Returns
        -------
        The configuration object corresponding to the specified object name.
        """
        for obj in self.config.get_objects():
            if obj.NAME == object_name:
                return obj
        return None

    def _get_contours(self, current_frame, next_frame):
        """
        Gets the contours from the frames.

        Parameters
        ----------
        current_frame : ndarray
            The current frame from the video capture.
        next_frame : ndarray
            The next frame from the video capture.

        Returns
        -------
        A list of contours detected between the current frame and the next frame.
        """
        return get_contours_from_frames(current_frame, next_frame)

    def _filter_contours(self, contours, object_name):
        """
        Filters contours from the frames based on the predefined area.

        Parameters
        ----------
        contours : list
            A list of contours detected from the frames.
        object_name : str
            The name of the object to use when filtering the contours.

        Returns
        -------
        A list of contours that fall within the predefined area for the specified object.
        """
        object_config = self._get_object_config(object_name)
        return filter_contours(contours, object_config.MIN_AREA, object_config.MAX_AREA)

    def _get_detections(self, contours, object_name, current_frame):
        """
        Gets detections from contours for a specific object.

        Parameters
        ----------
        contours : list
            A list of contours detected from the frames.
        object_name : str
            The name of the object for which detections should be obtained.
        current_frame : ndarray
            The current frame from the video capture.

        Returns
        -------
        A list of detections obtained from the contours for the specified object.
        """
        object_config = self._get_object_config(object_name)
        return [Detection(current_frame, contour, object_config) for contour in contours]

    def process_frame(self, current_frame, next_frame):
        """
        Analyzes a pair of video frames to identify and track objects of interest.

        Parameters
        ----------
        current_frame : ndarray
            The current frame from the video capture.
        next_frame : ndarray
            The next frame from the video capture.

        Returns
        -------
        contours : list
            A list of contours detected between the current frame and the next frame.
        recognized_objects_all : list
            A list of recognized objects identified in the current frame.
        """
        contours = self._get_contours(current_frame, next_frame)

        recognized_objects_all = []

        for object_name, tracker in self.trackers.items():
            filtered_contours = self._filter_contours(contours, object_name)
            detections = self._get_detections(filtered_contours, object_name, current_frame)
            tracker.track(current_frame)
            filtered_detections = tracker.filter_detections(detections)
            recognized_objects = self.validators[object_name].validate(filtered_detections, current_frame)
            tracker.add(recognized_objects)

            recognized_objects_all.extend(recognized_objects)

        return contours, recognized_objects_all

    def handle_mouse_event(self, event, x, y, flags, param):
        """
        Handles mouse events on the video frame. This method should be customized to suit your application.
        :param event: The mouse event.
        :param x: The x-coordinate of the mouse event.
        :param y: The y-coordinate of the mouse event.
        :param flags: Any relevant flags for the mouse event.
        :param param: Any additional parameters for the mouse event.
        """
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
            self._save_image_based_on_classification(event, x, y)
    
    def _save_image_based_on_classification(self, event, x, y):
        """
        Saves the image of the selected recognized object based on the classification (correct or wrong).
        """
        selected_object, selected_tracker = self._find_selected_object(x, y)

        if selected_object is not None and selected_tracker is not None:
            image = selected_object.clip.image
            classification = "true" if event == cv2.EVENT_LBUTTONDOWN else "false"

            object_config = selected_tracker.config
            dataset_folder = object_config.DATASET_FOLDER

            current_id = self._get_last_id(dataset_folder) + 1

            filename = f"{current_id}_{classification}.png"
            save_path = os.path.join(dataset_folder, filename)
            cv2.imwrite(save_path, image)

            selected_tracker.current_id = current_id + 1

            print(f"Saved image: {filename}")
    
    def _get_last_id(self, dataset_folder):
        """
        Retrieves the last ID used in the specified dataset folder.
        """
        files = os.listdir(dataset_folder)
        ids = []

        for file in files:
            if file.endswith(("_true.png", "_false.png")):
                id_str = file.split("_")[0]
                try:
                    id_num = int(id_str)
                    ids.append(id_num)
                except ValueError:
                    pass

        if ids:
            return max(ids)
        else:
            return 0

    def _find_selected_object(self, x, y):
        """
        Finds the recognized object that contains the selected point.
        """
        for object_name, tracker in self.trackers.items():
            for recognized_object in tracker.recognized_objects:
                bbox = recognized_object.get_bounding_coords()
                if x >= bbox[0] and y >= bbox[1] and x <= bbox[2] and y <= bbox[3]:
                    return recognized_object, tracker

        return None, None