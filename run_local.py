import cv2

from src.app import App

if __name__ == '__main__':
    #path = "assets\\video.mp4"
    #config = "config\\basic.yaml"
    
    #path = "assets\\video_thyssen.mp4"
    #config = "config\\thyssen_krupp.yaml"

    #path = "assets\\video_clips.mp4"
    #config = "config\\clips.yaml"

    path = 0
    config = "config\\webcam.yaml"

    app = App(path, config)

    while app.is_opened():
        app.process_frame()

        if cv2.waitKey(40) == 27:
            app.release_resources()    

