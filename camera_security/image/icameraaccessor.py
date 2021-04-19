# icameraaccessor.py | camera-security-rpi
# Describes the ICameraAccessor interface for accessing the camera to get data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.image.frame import Frame


class ICameraAccessor(ABC):

    @abstractmethod
    def GetFrame(self) -> Frame:
        """
        Returns the last frame that is cached. This should be used when sending frame to client
        """
        raise NotImplementedError()

    @abstractmethod
    def GetNewFrame(self) -> Frame:
        """
        Returns the newest frame from the camera.
        """
        raise NotImplementedError()
