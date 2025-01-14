
"""
Camera module, configures the webcam if it is avaialbe uses the
cv2 library from opencv-python-headless
Author: Gary Twinn
"""

from base64 import b64encode
import cv2
from logmanager import logger
from app_control import settings


class VideoCamera:
    """
    Initializes the VideoCamera class.

    The constructor creates a VideoCapture object, which represents the video source. It sets the video source
    properties, such as frame rate, width, height, brightness, and contrast. If no video camera is found, an
    error message is logged.

    """
    def __init__(self):
        self.video = cv2.VideoCapture(settings['cameraID'])
        if not self.video.isOpened():
            logger.error('VideoCameraClass: No video camera found')
        else:
            logger.info('VideoCameraClass: Starting video camera')
            self.video.set(cv2.CAP_PROP_FPS, settings['cameraFPS'])
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, settings['cameraWidth'])
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, settings['cameraHeight'])
            self.video.set(cv2.CAP_PROP_BRIGHTNESS, settings['cameraBrightness'])
            self.video.set(cv2.CAP_PROP_CONTRAST, settings['cameraContrast'])
            self.video.set(cv2.CAP_PROP_SATURATION, settings['cameraSaturation'])
            self.video.set(cv2.CAP_PROP_HUE, settings['cameraHue'])
            self.video.set(cv2.CAP_PROP_GAMMA, settings['cameraGamma'])
            self.video.set(cv2.CAP_PROP_GAIN, settings['cameraGain'])
            self.video.set(cv2.CAP_PROP_SHARPNESS, settings['cameraSharpness'])
            logger.info('Video FPS %s', self.video.get(cv2.CAP_PROP_FPS))
            logger.info('Video Width %s', self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            logger.info('Video Height %s', self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info('Video Backend %i', self.video.get(cv2.CAP_PROP_BACKEND))
            logger.info('Video Brightness %i', self.video.get(cv2.CAP_PROP_BRIGHTNESS))
            logger.info('Video Contrast %i', self.video.get(cv2.CAP_PROP_CONTRAST))
            logger.info('Video Saturation %i', self.video.get(cv2.CAP_PROP_SATURATION))
            logger.info('Video Sharpness %i', self.video.get(cv2.CAP_PROP_SHARPNESS))
            logger.info('Video Hue %i', self.video.get(cv2.CAP_PROP_HUE))
            logger.info('Video Gamma %i', self.video.get(cv2.CAP_PROP_GAMMA))
            logger.info('Video Gain %i', self.video.get(cv2.CAP_PROP_GAIN))


    def __del__(self):
        """Releases resources when app is closed down"""
        self.video.release()

    def get_frame(self):
        """Get a stream of raw images and encode as jpg files"""
        _ , frame = self.video.read()
        _ , jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_image(self):
        """Get a single image and send as a base64 encoded png file"""
        _ , frame = self.video.read()
        _ , jpeg = cv2.imencode(settings['cameraImageFormat'], frame)
        return b64encode(jpeg.tobytes()).decode()

    def mpeg_stream(self):
        """Image processor, converts the stream of jpegs into an m-jpeg format for the browser"""
        while True:
            frame = self.get_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


video_stream = VideoCamera()
