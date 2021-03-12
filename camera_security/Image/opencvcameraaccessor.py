# opencvcameraaccessor.py | camera-security-rpi
# Implements the ICameraAccessor interface using the OpenCV library
# Author: Lukas Žaromskis

import cv2
from camera_security.Image.frame import Frame
from camera_security.Image.icameraaccessor import ICameraAccessor


class OpenCVCameraAccessor(ICameraAccessor):

    def __init__(self, camera_id: int, frame_width: int, frame_height: int, use_minimal_buffer: bool = True):
        self.capture_device = cv2.VideoCapture(camera_id)
        if use_minimal_buffer:
            self.capture_device.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Set buffer size to 1 to get the latest frame from the camera
        self.capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    def GetFrame(self) -> Frame:
        ret, frame_data = self.capture_device.read()
        if not ret:
            raise RuntimeError()
        return Frame(frame_data)
