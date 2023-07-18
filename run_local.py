import cv2
import asyncio

from src.app import App

def main():
    #path = "assets\\video.mp4"
    #config = "config\\basic.yaml"
    
    #path = "assets\\video_thyssen.mp4"
    #config = "config\\thyssen_krupp.yaml"

    #path = "assets\\video_clips.mp4"
    #config = "config\\clips.yaml"

    video_path = "assets\\road_traffic.mp4"
    config_file = "config\\road.yaml"

    #path = 0
    #config = "config\\webcam.yaml"

    app = App()
    app.start_job(video_path, config_file)

if __name__ == '__main__':
    main()

