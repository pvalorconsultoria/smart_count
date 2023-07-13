import threading

import cv2
from flask import Flask, Response
from flask import send_from_directory
from flask import request
from src.app import App
from src.api.api import Api

class WebApplication:
    """
    A class to encapsulate a Flask application that shows the video stream in a web browser.
    """

    def __init__(self):
        """
        Constructor to initialize the Flask application.
        """
        path = "assets\\video_thyssen.mp4"
        config = "config\\thyssen_krupp.yaml"

        self.app = App(path, config)
        self.static_folder = 'C:\\Users\\diego\\Code\\OpenCV\\client\\build'

        self.api = Api()

        self.flask_app = Flask(
            __name__, 
            static_folder=self.static_folder,
            static_url_path='/static'
        )

        # Set processing thread to None initially
        self.processing_thread = None

        @self.flask_app.route('/')
        def index():
            """Video streaming home page."""
            return send_from_directory(self.static_folder, "index.html")

        @self.flask_app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return Response(self._generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.flask_app.route('/build/<path:path>')
        def serve_static(path):
            """Serve static files."""
            return send_from_directory(self.static_folder, path)

        @self.flask_app.route('/api/processedBatches')
        def processed_batches():
            return self.api.get_processed_batches()

        @self.flask_app.route('/api/processVideo', methods=['POST'])
        def process_video():
            """Handle the POST request for video processing."""
            # Stop current processing thread if it exists and is alive
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join()

            # Get data sent as JSON and perform processing
            data = request.get_json()
            print(data)

            self.app = App(path, config)

            # Start new processing thread
            self._start_processing()
            return {'status': 'success'}, 200

    def _generate_frames(self):
        """
        Generate frames for video streaming from the App instance.
        """
        while self.app.is_opened():
            frame = self.app.current_frame.copy()

            if frame is not None:
                _, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def _start_processing(self):
        # If processing is already running, do nothing
        if self.processing_thread and self.processing_thread.is_alive():
            return

        # Create and start new processing thread
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
        self.flask_app.run(threaded=True)
