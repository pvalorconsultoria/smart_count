
from src.frame import Frame
from src.tasks.task import AbstractTask

from transformers import YolosImageProcessor, YolosForObjectDetection
import torch

class YoloObjectCounting(AbstractTask):
    def __init__(self):
        super().__init__()
    
        self._model = None
        self._image_processor = None

    def process_frame(self, frame: Frame):
        image = frame.current_frame

        inputs = self._image_processor(images=image, return_tensors="pt")
        outputs = self._model(**inputs)

        target_sizes = torch.tensor([image.shape[:2]])
        results = self._image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        return results

    def preload(self):
        self._model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        self._image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    def release(self):
        pass