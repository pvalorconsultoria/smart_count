from src.config import ObjectConfig

def calculate_iou(box_a, box_b):
    """Calculate the Intersection over Union (IoU) of two bounding boxes."""
    # Determine the coordinates of the intersection rectangle
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    # Compute the area of intersection rectangle
    inter_area = max(0, x_b - x_a + 1) * max(0, y_b - y_a + 1)

    # Compute the area of both the prediction and ground-truth rectangles
    box_a_area = (box_a[2] - box_a[0] + 1) * (box_a[3] - box_a[1] + 1)
    box_b_area = (box_b[2] - box_b[0] + 1) * (box_b[3] - box_b[1] + 1)

    iou = inter_area / float(box_a_area + box_b_area - inter_area) if box_a_area + box_b_area - inter_area > 0 else 0.0

    return iou


def do_overlap(box_a, box_b):
    """Check if two bounding boxes overlap."""
    return box_a[0] <= box_b[2] and box_a[2] >= box_b[0] and box_a[1] <= box_b[3] and box_a[3] >= box_b[1]


class ObjectTracker:
    def __init__(self, object_config: ObjectConfig) -> None:
        self.config = object_config
        self.recognized_objects = []
        self.counter = 0

    def add(self, recognized_objects):
        """Add recognized objects to the tracker."""
        recognized_objects = [recognized_objects] if not isinstance(recognized_objects, list) else recognized_objects

        for recognized_object in recognized_objects:
            self.counter += 1
            recognized_object.count = self.counter
            self.recognized_objects.append(recognized_object)

    def track(self, frame):
        """Track recognized objects in the frame."""
        delete_indexes = []

        for idx, recognized_object in enumerate(self.recognized_objects):
            recognized_object.track(frame)

            if recognized_object.lost_track:
                delete_indexes.append(idx)

        self.recognized_objects = [v for k, v in enumerate(self.recognized_objects) 
                                   if k not in delete_indexes]

    def filter_detections(self, detections):
        filtered_detections = []
        
        for detection in detections:
            new_clips = []
            
            for clip in detection.clips:
                if clip is None:
                    continue

                overlap = False
                dc_bbox = clip.get_bounding_coords()

                for recognized_object in self.recognized_objects:
                    ro_bbox = recognized_object.get_bounding_coords()

                    if calculate_iou(dc_bbox, ro_bbox) > 0.05:
                        overlap = True
                        break

                if not overlap:
                    new_clips.append(clip)

            if new_clips:
                detection.clips = new_clips
                filtered_detections.append(detection)

        return filtered_detections