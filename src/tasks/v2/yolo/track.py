import cv2

from dataclasses import dataclass

from typing import Any

from src.frame import Frame
from src.tasks.task import AbstractTask

from src.tasks.v2.yolo.yolo8 import YoloPrediction
from src.tasks.v2.yolo.yolo8 import Prediction

@dataclass
class TrackedObject:
    id: int
    cluster: list[Prediction]

    bbox: Any

    center_x: int
    center_y: int

    speed_x: float
    speed_y: float

    acceleration_x: float
    acceleration_y: float

    dir_x: float
    dir_y: float

    hist: Any

    def draw(self, frame: Frame):
        x, y, w, h = self.bbox

        cv2.rectangle(frame.current_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

class ObjectTracker:
    def __init__(self) -> None:
        self._tracked_objects = {}
        self._unique_objects = 0

        self._max_iou = 0.5
        self._max_hist_similarity = 0.7

        self._next_object_id = 1 

    def process_predictions(self, frame: Frame, yolo_predictions: list[YoloPrediction]):
        frame_number_delta = frame["frame_number_delta"]

        clusters = []

        for yolo_prediction in yolo_predictions:
            for prediction in yolo_prediction.predictions:
                new_cluster = None

                for cluster in clusters:
                    for existing_prediction in cluster:
                        iou = self.calculate_iou(existing_prediction.bbox, prediction.bbox)

                        hist1 = self.calculate_color_histogram(prediction.frame.array(), prediction.bbox) 
                        hist2 = self.calculate_color_histogram(existing_prediction.frame.array(), existing_prediction.bbox) 

                        hist_sim = self.calculate_histogram_similarity(hist1, hist2)

                        if iou >= self._max_iou and hist_sim >= self._max_hist_similarity:
                            new_cluster = cluster
                            break
                    
                    if new_cluster:
                        break
                
                if not new_cluster:
                    new_cluster = []
                    clusters.append(new_cluster)
        
                new_cluster.append(prediction)

        new_objects_to_track = []

        for cluster in clusters:
            # Number of frames and speed/acceleration should be calculated pixels/frames
            time_interval = len(cluster)

            # Calculate the center points of the first and last predictions in the cluster
            first_center_x = cluster[0].bbox[0] + cluster[0].bbox[2] / 2
            first_center_y = cluster[0].bbox[1] + cluster[0].bbox[3] / 2

            last_center_x = cluster[-1].bbox[0] + cluster[-1].bbox[2] / 2
            last_center_y = cluster[-1].bbox[1] + cluster[-1].bbox[3] / 2

            # Calculate speed and acceleration based on the first and last centers
            speed_x, speed_y = self.calculate_speed((first_center_x, first_center_y), (last_center_x, last_center_y), time_interval)
            acceleration_x, acceleration_y = self.calculate_acceleration((0, 0), (speed_x, speed_y), time_interval)
            cluster_dir_x, cluster_dir_y = self.calculate_direction_vector(cluster)


            final_bbox = self.calculate_new_bounding_box(
                cluster[-1].bbox, 
                (last_center_x, last_center_y), 
                (acceleration_x, acceleration_y), 
                (cluster_dir_x, cluster_dir_y),
                frame_number_delta
            )

            cluster_hist = self.calculate_color_histogram(cluster[-1].frame.array(), cluster[-1].bbox)

            is_already_tracked = False

            for id, tracked_object in self._tracked_objects.items():
                iou = self.calculate_iou(final_bbox, tracked_object.bbox)
                hist_sim = self.calculate_histogram_similarity(cluster_hist, tracked_object.hist)

                if iou >= self._max_iou and hist_sim >= self._max_hist_similarity:
                    is_already_tracked = True

                    tracked_object.speed_x = speed_x
                    tracked_object.speed_y = speed_y
                    tracked_object.acceleration_x = acceleration_x
                    tracked_object.acceleration_y = acceleration_y
                    tracked_object.dir_x = cluster_dir_x
                    tracked_object.dir_y = cluster_dir_y
                    tracked_object.hist = cluster_hist

            if not is_already_tracked:
                tracked_object = TrackedObject(
                    id=self._next_object_id,
                    cluster=cluster,
                    bbox=cluster[-1].bbox,
                    center_x=last_center_x,
                    center_y=last_center_y,
                    speed_x=speed_x,
                    speed_y=speed_y,
                    acceleration_x=acceleration_x,
                    acceleration_y=acceleration_y,
                    dir_x=cluster_dir_x,
                    dir_y=cluster_dir_y,
                    hist=cluster_hist
                )

                new_objects_to_track.append(tracked_object)

        for tracked_object in new_objects_to_track:
            self._tracked_objects[self._next_object_id] = tracked_object

            self._next_object_id += 1

    def update_trackers(self):
        for idx, tracked_object in self._tracked_objects.items():
            initial_bbox = tracked_object.bbox
            initial_center = (tracked_object.center_x, tracked_object.center_y)
            acceleration = (tracked_object.acceleration_x, tracked_object.acceleration_y)
            direction = (tracked_object.dir_x, tracked_object.dir_y)

            final_bbox = self.calculate_new_bounding_box(initial_bbox, initial_center, acceleration, direction, 1)
            final_center_x, final_center_y = self.calculate_bounding_box_center(final_bbox)

            tracked_object.bbox = final_bbox
            tracked_object.center_x = final_center_x
            tracked_object.center_y = final_center_y


    def draw_objects(self, frame: Frame):
        for _, tracked_object in self._tracked_objects.items():
            tracked_object.draw(frame)

    def calculate_direction_vector(self, cluster):
        """
        Calculate the direction vector from the first to the last center in the cluster.
        :param cluster: List of YoloPrediction objects representing the cluster of bounding boxes.
        :return: Tuple (dir_x, dir_y) representing the direction vector.
        """
        first_prediction = cluster[0]
        last_prediction = cluster[-1]

        first_center_x, first_center_y = self.calculate_bounding_box_center(first_prediction.bbox)
        last_center_x, last_center_y = self.calculate_bounding_box_center(last_prediction.bbox)

        dir_x = last_center_x - first_center_x
        dir_y = last_center_y - first_center_y

        return dir_x, dir_y

    def calculate_bounding_box_center(self, bbox):
        """
        Calculate the center coordinates (x, y) of a bounding box.
        :param bbox: Tuple (x, y, w, h) representing the bounding box's top-left corner coordinates (x, y)
                    and its width (w) and height (h).
        :return: Tuple (center_x, center_y) representing the center coordinates of the bounding box.
        """
        x, y, w, h = bbox
        center_x = x + w // 2
        center_y = y + h // 2
        return center_x, center_y

    def calculate_new_bounding_box(self, initial_bbox, initial_center, acceleration, direction_vector, delta_t):
        """
        Calculate the new bounding box based on speed, acceleration, and direction vector over a time interval (delta t).
        :param initial_bbox: Tuple (x0, y0, w0, h0) representing the initial bounding box.
        :param initial_center: Tuple (x0, y0) representing the initial center of the bounding box.
        :param acceleration: Tuple (accel_x, accel_y) representing the acceleration in the x and y directions.
        :param direction_vector: Tuple (dir_x, dir_y) representing the direction vector from the first to the last center.
        :param delta_t: Time interval in frames for which to calculate the new bounding box.
        :return: Tuple (x_t, y_t, w_t, h_t) representing the new bounding box at time t=delta_t.
        """
        x0, y0, w0, h0 = initial_bbox
        x0_center, y0_center = initial_center
        accel_x, accel_y = acceleration
        dir_x, dir_y = direction_vector

        # Calculate the new center position at time t=delta_t using the direction vector
        x_t_center = x0_center + dir_x * delta_t + 0.5 * accel_x * delta_t**2
        y_t_center = y0_center + dir_y * delta_t + 0.5 * accel_y * delta_t**2

        # Calculate the new bounding box's (x, y) position using the center
        x_t = int(x_t_center - w0 / 2)  # Assuming w0 is the width of the bounding box
        y_t = int(y_t_center - h0 / 2)  # Assuming h0 is the height of the bounding box

        # The size of the bounding box remains unchanged
        w_t = w0
        h_t = h0

        return x_t, y_t, w_t, h_t

    def calculate_cluster_center(self, cluster, alpha=0.2):
        """
        Calculate the center of a cluster of bounding boxes using Exponential Moving Average (EMA).
        :param cluster: List of YOLOPrediction objects representing the cluster.
        :param alpha: Smoothing factor (between 0 and 1) for EMA.
        :return: Tuple (center_x, center_y) representing the estimated center.
        """
        prev_center_x = sum([prediction.bbox[0] + prediction.bbox[2] / 2 for prediction in cluster]) / len(cluster)
        prev_center_y = sum([prediction.bbox[1] + prediction.bbox[3] / 2 for prediction in cluster]) / len(cluster)

        for prediction in cluster:
            current_center_x = prediction.bbox[0] + prediction.bbox[2] / 2
            current_center_y = prediction.bbox[1] + prediction.bbox[3] / 2

            # Exponential Moving Average to update the center coordinates
            center_x = alpha * current_center_x + (1 - alpha) * prev_center_x
            center_y = alpha * current_center_y + (1 - alpha) * prev_center_y

            # Update the previous center for the next iteration
            prev_center_x, prev_center_y = center_x, center_y

        return center_x, center_y

    def calculate_speed(self, prev_center, current_center, time_interval):
        """
        Calculate the speed of an object based on the change in position over time.
        :param prev_center: Tuple (x, y) representing the center position in the previous frame.
        :param current_center: Tuple (x, y) representing the center position in the current frame.
        :param time_interval: Time interval between the previous and current frames.
        :return: Tuple (speed_x, speed_y) representing the speed in the x and y directions.
        """
        delta_x = current_center[0] - prev_center[0]
        delta_y = current_center[1] - prev_center[1]

        speed_x = delta_x / time_interval
        speed_y = delta_y / time_interval

        return speed_x, speed_y

    def calculate_acceleration(self, prev_speed, current_speed, time_interval):
        """
        Calculate the acceleration of an object based on the change in speed over time.
        :param prev_speed: Tuple (speed_x, speed_y) representing the speed in the previous frame.
        :param current_speed: Tuple (speed_x, speed_y) representing the speed in the current frame.
        :param time_interval: Time interval between the previous and current frames.
        :return: Tuple (accel_x, accel_y) representing the acceleration in the x and y directions.
        """
        delta_speed_x = current_speed[0] - prev_speed[0]
        delta_speed_y = current_speed[1] - prev_speed[1]

        acceleration_x = delta_speed_x / time_interval
        acceleration_y = delta_speed_y / time_interval

        return acceleration_x, acceleration_y

    def calculate_iou(self, box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        xA = max(x1, x2)
        yA = max(y1, y2)
        xB = min(x1 + w1, x2 + w2)
        yB = min(y1 + h1, y2 + h2)

        inter_area = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        box1_area = w1 * h1
        box2_area = w2 * h2
        iou = inter_area / float(box1_area + box2_area - inter_area)

        return iou

    def calculate_color_histogram(self, frame, box):
        x, y, w, h = box
        roi = frame[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        hist_hue = cv2.calcHist([hsv_roi], [0], None, [256], [0, 256])
        hist_hue = cv2.normalize(hist_hue, hist_hue, 0, 255, cv2.NORM_MINMAX)
        return hist_hue

    def calculate_histogram_similarity(self, hist1, hist2):
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

class TrackYoloDetectionsTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self._object_tracker = ObjectTracker()

    def _draw_objects(self, frame):
        self._object_tracker.draw_objects()

    def run(self, frame: Frame = None) -> Frame:
        if frame["yolo_predictions"]:
            self._object_tracker.process_predictions(frame, frame["yolo_predictions"])

        self._object_tracker.update_trackers()

        self._object_tracker.draw_objects(frame)

        return frame
