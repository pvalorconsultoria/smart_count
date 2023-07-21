from src.frame import Frame
from src.tasks.task import AbstractTask

class Pipeline:
    def __init__(self, tasks: list[AbstractTask]) -> None:
        self.tasks = tasks
    
    def run(self) -> Frame:
        result = None
        for task in self.tasks:
            result = task.run(result)
        return result

    def release(self):
        for task in self.tasks:
            task.release()