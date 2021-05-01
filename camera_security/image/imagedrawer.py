# imagedrawer.py | camera-security-rpi
# Implements the IImageDrawer interface for drawing on images
# Author: Lukas Žaromskis

import cv2
from typing import Tuple, Optional

from numpy import ndarray

from camera_security.image.frame import Frame
from camera_security.image.iimagedrawer import IImageDrawer
from camera_security.utility.boundingbox import BoundingBox


class ImageDrawer(IImageDrawer):

    def DrawRectangle(self, frame: Frame, bounds: BoundingBox, colour: Tuple[int, int, int], thickness: int):
        data = frame.GetData()
        height, width = ImageDrawer.__GetDimensions(data)

        top_left, bottom_right = bounds.GetCoordinatesInPixels(width, height)
        cv2.rectangle(data, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), colour, thickness)

    def DrawText(self, frame: Frame, text: str, pos: Tuple[float, float], font: int, font_scale: int, font_thickness: int,
                 text_colour: Tuple[int, int, int], background_colour: Optional[Tuple[int, int, int]]):
        data = frame.GetData()
        height, width = ImageDrawer.__GetDimensions(data)
        width_pixels = int(pos[0] * width)
        height_pixels = int(pos[1] * height)
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        start_pos = (width_pixels - text_w, height_pixels - text_h)
        end_pos = (width_pixels, height_pixels)
        if background_colour is not None:
            cv2.rectangle(data, start_pos, end_pos, background_colour, -1)
        cv2.putText(data, text, start_pos, font, font_scale, text_colour, font_thickness)

    @staticmethod
    def __GetDimensions(data: ndarray) -> Tuple[int, int]:
        dimensions = data.shape
        return dimensions[0], dimensions[1]
