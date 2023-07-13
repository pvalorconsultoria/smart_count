import threading

import cv2
from flask import Flask, render_template, Response
from src.app import App

class WebApplication:
    """
    A class to encapsulate a Flask application that shows the video stream in a web browser.
    """

    def __init__(self, app: App, template_folder: str):
        """
        Constructor to initialize the Flask application.
        :param app: An instance of the App class.
        :param template_folder: Path to the folder with Flask templates.
        """
        self.app = app
        self.template_folder = template_folder
        self.flask_app = Flask(__name__, template_folder=self.template_folder)

        @self.flask_app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        @self.flask_app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return Response(self._generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def _generate_frames(self):
        """
        Generate frames for video streaming from the App instance.
        """
        while self.app.is_opened():
            print("Aqui")
            frame = self.app.current_frame.copy()

            if frame is not None:
                _, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def _start_processing(self):
        self.processing_thread = threading.Thread(target=self._process_app_frames, daemon=True)
        self.processing_thread.start()

    def _process_app_frames(self):
        """
        Process frames in a loop using the App instance.
        """
        while self.app.is_opened():
            self.app.process_frame()

    def run(self):
        """
        Runs the Flask application.
        """
        self._start_processing()
        self.flask_app.run(threaded=True)
