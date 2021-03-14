# resultfilterbycertainty.py | camera-security-rpi
# Implements the IFrameProcessor interface in class ResultFilterByCertainty to filter out results based on their certainty
# Author: Lukas Žaromskis

from typing import List
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iresultfilter import IResultFilter


class ResultFilterByCertainty(IResultFilter):

    def __init__(self, certainty_threshold: float):
        self.certainty_threshold = certainty_threshold

    def Filter(self, data: List[DetectionData]) -> List[DetectionData]:
        filtered_list = list()

        for item in data:
            if item.GetCertainty() >= self.certainty_threshold:
                filtered_list.append(item)

        return filtered_list
