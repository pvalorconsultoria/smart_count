import queue
import datetime

class Frame:
    def __init__(self, current_frame, next_frame):
        self.timestamp = datetime.datetime.now()
        self.current_frame = current_frame
        self.next_frame = next_frame

class FrameQueue(queue.Queue):
    pass
