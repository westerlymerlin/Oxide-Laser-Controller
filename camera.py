"""
Camera Control and Image Capture

This module provides functionality for controlling and capturing images from a camera device.
Handles camera setup, configuration, image acquisition, and cleanup operations.

Features:
    - Camera initialization and configuration
    - Image capture and storage
    - Camera parameter adjustments (exposure, resolution, etc.)
    - Resource management (proper camera shutdown)

Usage Example:
    from camera import Camera

    camera = Camera()
    camera.capture('image.jpg')
    camera.close()

The module is designed for use with hardware camera interfaces and ensures proper
resource handling for stable operation in long-running applications.

Dependencies:
    Hardware: Compatible camera device
    Software: Appropriate camera drivers/libraries
"""

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
    def __init__(self, camera_index, camerasettings):
        self.video = cv2.VideoCapture(camerasettings['cameraID'])
        if not self.video.isOpened():
            logger.error('VideoCameraClass: No video camera found instance=%s', camera_index)
        else:
            logger.info('VideoCameraClass: Starting video camera %s as video_camera_instance_%s', camerasettings['cameraID'], camera_index)
            self.video.set(cv2.CAP_PROP_FPS, camerasettings['cameraFPS'])
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, camerasettings['cameraWidth'])
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, camerasettings['cameraHeight'])
            self.video.set(cv2.CAP_PROP_BRIGHTNESS, camerasettings['cameraBrightness'])
            self.video.set(cv2.CAP_PROP_CONTRAST, camerasettings['cameraContrast'])
            self.video.set(cv2.CAP_PROP_SATURATION, camerasettings['cameraSaturation'])
            self.video.set(cv2.CAP_PROP_HUE, camerasettings['cameraHue'])
            self.video.set(cv2.CAP_PROP_GAMMA, camerasettings['cameraGamma'])
            self.video.set(cv2.CAP_PROP_GAIN, camerasettings['cameraGain'])
            self.video.set(cv2.CAP_PROP_SHARPNESS, camerasettings['cameraSharpness'])
            logger.info('camera%s Video FPS %s', camera_index, self.video.get(cv2.CAP_PROP_FPS))
            logger.info('camera%s Video Width %s', camera_index, self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            logger.info('camera%s Video Height %s', camera_index, self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info('camera%s Video Backend %i', camera_index, self.video.get(cv2.CAP_PROP_BACKEND))
            logger.info('camera%s Video Brightness %i', camera_index, self.video.get(cv2.CAP_PROP_BRIGHTNESS))
            logger.info('camera%s Video Contrast %i', camera_index, self.video.get(cv2.CAP_PROP_CONTRAST))
            logger.info('camera%s Video Saturation %i', camera_index, self.video.get(cv2.CAP_PROP_SATURATION))
            logger.info('camera%s Video Sharpness %i', camera_index, self.video.get(cv2.CAP_PROP_SHARPNESS))
            logger.info('camera%s Video Hue %i', camera_index, self.video.get(cv2.CAP_PROP_HUE))
            logger.info('camera%s Video Gamma %i', camera_index, self.video.get(cv2.CAP_PROP_GAMMA))
            logger.info('camera%s Video Gain %i', camera_index, self.video.get(cv2.CAP_PROP_GAIN))


    def __del__(self):
        """Releases resources when app is closed down"""
        self.video.release()

    def get_frame(self):
        """Get a stream of raw images and encode as jpg files"""
        _ , frame = self.video.read()
        _ , jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def mpeg_stream(self):
        """Image processor, converts the stream of jpegs into an m-jpeg format for the browser"""
        while True:
            frame = self.get_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


video_camera_instance_0 = VideoCamera(0, settings['camera0'])
video_camera_instance_1 = VideoCamera(1, settings['camera1'])
