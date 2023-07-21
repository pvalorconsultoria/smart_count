import cv2
import visdom
import numpy as np

from src.tasks import AbstractTask
from src.frame import Frame

class VideoLocalViewerTask(AbstractTask):
    def __init__(self, job) -> None:
        super().__init__(job)

        self.vis = visdom.Visdom()
    
    def run(self, frame: Frame = None) -> Frame:
        image = frame.array()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.moveaxis(image, 2, 0)

        self.vis.image(image, win='result_image', opts={'title':'result_image', 'jpgquality':10})

        return frame

    def release(self):
        self.vis.close()