# opencvcameraaccessor.py | camera-security-rpi
# Implements the ICameraAccessor interface using the OpenCV library
# Author: Lukas Žaromskis

from threading import Lock
import cv2
from camera_security.image.frame import Frame
from camera_security.image.icameraaccessor import ICameraAccessor


class OpenCVCameraAccessor(ICameraAccessor):

    def __init__(self, camera_id: int, frame_width: int, frame_height: int, use_minimal_buffer: bool = True):
        self.__lastFrame = None
        self.__lock = Lock()
        self.__capture_device = cv2.VideoCapture(camera_id)
        if use_minimal_buffer:
            self.__capture_device.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Set buffer size to 1 to get the latest frame from the camera
        self.__capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.__capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    def GetFrame(self) -> Frame:
        self.__lock.acquire()
        frame_data = self.__lastFrame
        self.__lock.release()
        return Frame(frame_data)

    def GetNewFrame(self) -> Frame:
        ret, frame_data = self.__capture_device.read()
        if not ret:
            raise RuntimeError()
        self.__lock.acquire()
        self.__lastFrame = frame_data
        self.__lock.release()
        frame = Frame(frame_data)
        return frame
