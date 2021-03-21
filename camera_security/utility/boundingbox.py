# boundingbox.py | camera-security-rpi
# Describes the BoundingBox class for storing bounding box data
# Author: Lukas Žaromskis

from typing import Tuple


class BoundingBox:

    def __init__(self, top_left_x: int, top_left_y: int, bottom_right_x: int, bottom_right_y: int):
        self.__top_left = (top_left_x, top_left_y)
        self.__bottom_right = (bottom_right_x, bottom_right_y)

    def IsColliding(self, other: 'BoundingBox') -> bool:
        """
        Checks if this bounding box collides with the given bounding box
        """
        return (self.__top_left[0] < other.__bottom_right[0] and self.__bottom_right[0] > other.__top_left[0] and
                self.__top_left[1] < other.__bottom_right[1] and self.__bottom_right[1] > other.__top_left[1])

    def GetCoordinates(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Returns the coordinates in a tuple.
        First element is top left corner.
        Second element is bottom right corner.
        Each corner contains the x and y coordinates
        """
        return self.__top_left, self.__bottom_right
