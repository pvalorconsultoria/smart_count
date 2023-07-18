import cv2
import datetime
import asyncio

class Frame:
    def __init__(self, timestamp, frame):
        self.timestamp = timestamp
        self.frame = frame

class FrameQueue(asyncio.Queue):
    pass

class FrameProcessor:
    def __init__(self, queue, model):
        self.queue = queue
        self.model = model
        self._running = True

    async def process_frame(self):
        while self._running:
            frame = await self.queue.get()

            print("Aqui 1")
            await asyncio.sleep(1)
            # apply YOLO model on the frame
            # result = self.model.predict(frame.frame)
            # do something with the result
            print("Aqui 2")

            self.queue.task_done()

    def stop(self):
        self._running = False

class FrameManager:
    def __init__(self, model, execution_mode='local'):
        self.queue = FrameQueue(maxsize=1)  # we only need to store one frame at a time
        self.processor = FrameProcessor(self.queue, model)
        self.execution_mode = execution_mode
        self._processor_task = None

    async def run_model_locally(self, frame):
        # run YOLO locally
        pass

    async def run_model_on_server(self, frame):
        # run YOLO on a server
        pass

    async def process_frame(self, current_frame):
        await self.queue.put(current_frame)  # Add the current frame to the queue

        if self.queue.qsize() == 1:  # Only process the frame if the queue has exactly one frame
            if self._processor_task is None or self._processor_task.done():
                self._processor_task = asyncio.create_task(self.processor.process_frame())

        # Wait for the frame processing to complete
        await self.queue.join()

class AsyncObjectCounting:
    def __init__(self, config):
        self.config = config
        self.frame_manager = FrameManager('yolo', 'server')
        self.lock = asyncio.Lock()

    async def process_frame(self, current_frame, next_frame):
        timestamp = datetime.datetime.now()
        frame = Frame(timestamp, current_frame)

        if not self.lock.locked():  # Only process the frame if the lock is not already acquired
            async with self.lock:  # This will block if a frame is currently being processed
                asyncio.create_task(self.frame_manager.process_frame(frame))

        return []

    def handle_mouse_event(self, event, x, y, flags, param):
        pass


