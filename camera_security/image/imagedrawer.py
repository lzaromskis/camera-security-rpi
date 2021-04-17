# imagedrawer.py | camera-security-rpi
# Implements the IImageDrawer interface for drawing on images
# Author: Lukas Žaromskis

import cv2
from typing import Tuple

from camera_security.image.frame import Frame
from camera_security.image.iimagedrawer import IImageDrawer
from camera_security.utility.boundingbox import BoundingBox


class ImageDrawer(IImageDrawer):
    def DrawRectangle(self, frame: Frame, bounds: BoundingBox, colour: Tuple[int, int, int], thickness: int):
        data = frame.GetData()
        dimensions = data.shape
        height = dimensions[0]
        width = dimensions[1]

        top_left, bottom_right = bounds.GetCoordinates()
        top_left_x = int(top_left[0] * width)
        top_left_y = int(top_left[1] * height)
        bottom_right_x = int(bottom_right[0] * width)
        bottom_right_y = int(bottom_right[1] * height)

        cv2.rectangle(data, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), colour, thickness)

