from abc import abstractmethod

from src.frame import Frame

class AbstractTask:
    def __init__(self, job) -> None:
        self.job = job

    @abstractmethod
    def run(self, frame: Frame = None) -> Frame:
        pass

    @abstractmethod
    def release(self):
        pass

class DummyTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)
    
    def run(self, frame: Frame = None) -> Frame:
        return frame
