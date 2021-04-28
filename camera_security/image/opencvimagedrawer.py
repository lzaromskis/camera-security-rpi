# imagedrawer.py | camera-security-rpi
# Implements the IImageDrawer interface for drawing on images
# Author: Lukas Žaromskis

import cv2
from typing import Tuple

from camera_security.image.frame import Frame
from camera_security.image.iimagedrawer import IImageDrawer
from camera_security.utility.boundingbox import BoundingBox


class OpenCVImageDrawer(IImageDrawer):
    def DrawRectangle(self, frame: Frame, bounds: BoundingBox, colour: Tuple[int, int, int], thickness: int):
        data = frame.GetData()
        dimensions = data.shape
        height = dimensions[0]
        width = dimensions[1]

        top_left, bottom_right = bounds.GetCoordinatesInPixels(width, height)
        cv2.rectangle(data, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), colour, thickness)
