import os
import cv2
import numpy as np
from src.detection import DetectionValidator, Detection
from src.tracker import ObjectTracker
from src.contour import get_contours_from_frames, filter_contours, Contour

from src.config import Config

class App:
    """
    A class used to encapsulate contour detection, object recognition and tracking in video frames.
    """

    def __init__(self, video_path: str, config_file: str):
        """
        Constructor to initialize video file, tracking and detection, and video capture if needed.
        :param video_path: Path to the video file.
        """
        self.config = Config(config_file)
        
        self._init_video(video_path)
        self._init_tracking_and_detection()
        self.should_capture_video = False
        self._init_capture_if_needed()

        # Register the mouse event handler
        if self.config.DISPLAY_WINDOW:
            cv2.namedWindow(self.config.FRAME_NAME)
            cv2.setMouseCallback(self.config.FRAME_NAME, self._handle_mouse_event)

    def _handle_mouse_event(self, event, x, y, flags, param):
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


    def _init_video(self, video_path: str):
        """
        Initializes video capture and reads the first two frames.
        """
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise Exception("Error opening video file")

        self.smart_count_logo = cv2.imread(self.config.SMARTCOUNT_LOGO_PATH)
        self.smart_count_logo = cv2.resize(self.smart_count_logo, (300, 70))

        _, self.current_frame = self.cap.read()
        _, self.next_frame = self.cap.read()

    def _init_tracking_and_detection(self):
        """
        Initializes detection validator and object tracker for each object in the configuration.
        """
        self.validators = {obj.NAME: DetectionValidator(obj) for obj in self.config.get_objects()}
        self.trackers = {obj.NAME: ObjectTracker(obj) for obj in self.config.get_objects()}

    def _init_capture_if_needed(self):
        """
        Initializes video capture if capturing video is enabled.
        """
        if self.should_capture_video:
            video_h, video_w, _ = self.current_frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video = cv2.VideoWriter(self.config.OUTPUT_VIDEO_PATH, fourcc, 30, (video_w, video_h))

    # Changes in process_frame and related methods
    def process_frame(self):
        """
        Main method to process a video frame - get contours, detections, recognized objects,
        and move on to the next frame.
        """
        contours = self._get_contours()

        for object_name, tracker in self.trackers.items():
            filtered_contours = self._filter_contours(contours, object_name)
            detections = self._get_detections(filtered_contours, object_name)
            tracker.track(self.current_frame)
            filtered_detections = tracker.filter_detections(detections)
            recognized_objects = self.validators[object_name].validate(filtered_detections, self.current_frame)
            tracker.add(recognized_objects)
            
        if self.config.DISPLAY_WINDOW:
            self._draw_frame(contours, recognized_objects)
            #self._draw_smart_count_logo()
            #self._draw_counter()

        self._capture_video()
        self._move_to_next_frame()

    def _get_object_config(self, object_name):
        """
        Retrieves the configuration for a specific object.
        """
        for obj in self.config.get_objects():
            if obj.NAME == object_name:
                return obj
        return None

    def _get_contours(self):
        """
        Gets the contours from the frames.
        """
        return get_contours_from_frames(self.current_frame, self.next_frame)

    def _filter_contours(self, contours, object_name):
        """
        Filters contours from the frames based on the predefined area.
        """
        object_config = self._get_object_config(object_name)
        return filter_contours(contours, object_config.MIN_AREA, object_config.MAX_AREA)

    def _get_detections(self, contours, object_name):
        """
        Gets detections from contours for a specific object.
        """
        # The Detection class or function should now also accept the configuration of the object as a parameter.
        # The detection model of the object can then be used to classify the contours.
        object_config = self._get_object_config(object_name)
        return [Detection(self.current_frame, contour, object_config) for contour in contours]

    def _draw_frame(self, contours, recognized_objects):
        """
        Draws frame with logo, counter and (optionally) contours and recognized objects.
        """        
        # Uncomment these if you want to draw contours and recognized objects
        # self._draw_contours(contours)
        # self._draw_recognized_objects(recognized_objects)
        cv2.imshow(self.config.FRAME_NAME, self.current_frame)

    def _draw_smart_count_logo(self):
        """
        Overlays the smart count logo on the current frame.
        """
        x, y, w, h = 0, 0, 300, 70 
        self.current_frame[y:y+h, x:x+w,:] = self.smart_count_logo

    def _draw_counter(self):
        """
        Draws the object counter on the current frame.
        """
        x, y = 310, 30
        tracker = list(self.trackers.values())[0]
        cv2.putText(self.current_frame, f"COUNT: {tracker.counter}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    def _draw_contours(self, contours):
        """
        Draws contours on the current frame.
        """
        for contour in contours:
            contour.draw(self.current_frame)
            contour.get_bounding_box().draw(self.current_frame)

    def _draw_recognized_objects(self, recognized_objects):
        """
        Draws recognized objects on the current frame.
        """
        for recognized_object in recognized_objects:
            recognized_object.draw()

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
