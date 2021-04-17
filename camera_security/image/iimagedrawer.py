# iimagedrawer.py | camera-security-rpi
# Describes the IImageDrawer interface for drawing on images
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import Tuple

from camera_security.image.frame import Frame
from camera_security.utility.boundingbox import BoundingBox


class IImageDrawer(ABC):

    @abstractmethod
    def DrawRectangle(self, frame: Frame, bounds: BoundingBox, colour: Tuple[int, int, int], thickness: int):
        """
        Draws a rectangle on the frame
        """
        raise NotImplementedError()
