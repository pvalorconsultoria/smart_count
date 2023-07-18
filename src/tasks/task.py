from abc import ABC, abstractmethod
from src.frame import Frame

class AbstractTask(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def process_frame(self, frame: Frame):
        pass

    @abstractmethod
    def preload(self):
        pass

    @abstractmethod
    def release(self):
        pass
