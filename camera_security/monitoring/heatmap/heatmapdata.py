# heatmapdata.py | camera-security-rpi
# Describes the HeatmapData class for storing heatmap data
# Author: Lukas Žaromskis
from typing import List

from camera_security.utility.boundingbox import BoundingBox


class HeatmapData:

    def __init__(self, bounding_boxes: List[BoundingBox], time: float):
        self.__bounding_boxes = bounding_boxes
        self.__time = time

    def GetBoundingBoxes(self):
        return self.__bounding_boxes

    def GetTime(self):
        return self.__time
