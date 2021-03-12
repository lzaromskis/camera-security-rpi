# icameraaccessor.py | camera-security-rpi
# Describes the ICameraAccessor interface for accessing the camera to get data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.Image.frame import Frame


class ICameraAccessor(ABC):

    @abstractmethod
    def GetFrame(self) -> Frame:
        """
        Gets a frame from the camera
        """
        raise NotImplementedError()
