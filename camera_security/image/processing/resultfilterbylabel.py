# resultfilterbylabel.py | camera-security-rpi
# Implements the IFrameProcessor interface in class ResultFilterByLabel to filter out results based on their labels
# Author: Lukas Žaromskis

from typing import List
from camera_security.image.processing.detectiondata import DetectionData
from camera_security.image.processing.iresultfilter import IResultFilter


class ResultFilterByLabel(IResultFilter):

    def __init__(self, label_whitelist: List[str]):
        self.label_whitelist = label_whitelist

    def Filter(self, data: List[DetectionData]) -> List[DetectionData]:
        filtered_list = list()

        for item in data:
            if item.GetLabel() in self.label_whitelist:
                filtered_list.append(item)

        return filtered_list
