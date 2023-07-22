import cv2

from src.frame import Frame
from src.tasks.task import AbstractTask

class TrackYoloDetectionsTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self._tracked_objects = []
        self._counted_objects = 0

    def _is_bbox_within_frame(self, bbox, frame_width, frame_height):
        x, y, w, h = bbox
        return 0 <= x < frame_width and 0 <= y < frame_height and x + w <= frame_width and y + h <= frame_height

    def _draw_bbox_on_frame(self, frame, bbox):
        x, y, w, h = map(int, bbox)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    def _bbox_overlap(self, bbox1, bbox2):
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        return x_overlap * y_overlap

    def _is_bbox_unique(self, bbox):
        for tracked_object in self._tracked_objects:
            if self._bbox_overlap(bbox, tracked_object["position"]) > 0:
                return False
        return True

    def _process_predictions(self, frame):
        self._counted_objects += len(frame["yolo_predictions"])

        for prediction in frame["yolo_predictions"]:
            # Check if the object is not already being tracked (based on overlap)
            if self._is_bbox_unique(prediction["bbox"]):

                tracker = cv2.legacy.TrackerMedianFlow_create()
                tracker.init(prediction["clip_frame"], prediction["bbox"])

                self._tracked_objects.append({
                    "prediction": prediction,
                    "position": prediction["bbox"],
                    "tracker": tracker
                })

    def _update_trackers(self, frame):
        # Create a new list to store the tracked objects that are within the frame
        valid_tracked_objects = []

        frame_height, frame_width = frame.array().shape[:2]

        for tracked_object in self._tracked_objects:
            tracker = tracked_object["tracker"]

            _, new_position = tracker.update(frame.current_frame)

            if self._is_bbox_within_frame(new_position, frame_width, frame_height):
                # The bounding box is within the frame, so update the tracked object's position
                tracked_object["position"] = new_position
                valid_tracked_objects.append(tracked_object)
                self._draw_bbox_on_frame(frame.current_frame, new_position)
            else:
                # The bounding box is outside the frame, so don't update its position (remove it)
                print("Object outside the frame, deleting it.")
                # You may want to perform some cleanup or additional actions here
                # For example, release the trackers or log the event

        # Update the list of tracked objects with only the valid ones
        self._tracked_objects = valid_tracked_objects

    def run(self, frame: Frame = None) -> Frame:
        if frame["yolo_predictions"]:
            self._process_predictions(frame)

        self._update_trackers(frame)

        return frame
