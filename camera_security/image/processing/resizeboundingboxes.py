# resizeboundingboxes.py | camera-security-rpi
# Implements the IResultFilter interface in class ResultFilterByLabel to change the size of the bounding box
# Author: Lukas Žaromskis
from typing import List

from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iresultfilter import IResultFilter
from camera_security.utility.boundingbox import BoundingBox


class ResizeBoundingBoxes(IResultFilter):

    def __init__(self, height_percentage: float):
        self.__height_percentage = height_percentage

    def Filter(self, data: List[DetectionData]) -> List[DetectionData]:
        new_list = list()
        for d in data:
            old_bb = d.GetBoundingBox()
            old_tl, old_br = old_bb.GetCoordinates()
            old_height = old_br[1] - old_tl[1]
            new_height = old_height * self.__height_percentage
            new_tl_y = old_br[1] - new_height
            new_bb = BoundingBox(old_tl[0], new_tl_y, old_br[0], old_br[1])
            new_list.append(DetectionData(new_bb, d.GetLabel(), d.GetCertainty()))
        return new_list
