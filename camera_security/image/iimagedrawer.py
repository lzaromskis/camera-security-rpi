# iimagedrawer.py | camera-security-rpi
# Describes the IImageDrawer interface for drawing on images
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import Tuple, Optional

from camera_security.image.frame import Frame
from camera_security.utility.boundingbox import BoundingBox


class IImageDrawer(ABC):

    @abstractmethod
    def DrawRectangle(self, frame: Frame, bounds: BoundingBox, colour: Tuple[int, int, int], thickness: int):
        """
        Draws a rectangle on the frame
        """
        raise NotImplementedError()

    @abstractmethod
    def DrawText(self, frame: Frame,
                 text: str,
                 pos: Tuple[float, float],
                 font: int,
                 font_scale: int,
                 font_thickness: int,
                 text_colour: Tuple[int, int, int],
                 background_colour: Optional[Tuple[int, int, int]]):
        """
        Draws text on the frame
        """
        raise NotImplementedError()