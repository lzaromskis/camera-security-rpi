# imagefacade.py | camera-security-rpi
# Describes the ImageFacade class for controlling the image getting and processing subsystem
# Author: Lukas Žaromskis
from camera_security.image.frame import Frame
from camera_security.image.opencvcameraaccessor import OpenCVCameraAccessor


class ImageFacade:

    def __init__(self):
        self.camera_accessor = OpenCVCameraAccessor(0, 640, 480)

    def GetFrame(self) -> Frame:
        return self.camera_accessor.GetNewFrame()
