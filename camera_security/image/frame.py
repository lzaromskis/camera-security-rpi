# iframeprocessor.py | camera-security-rpi
# Describes the Frame class for storing frame information
# Author: Lukas Žaromskis

import numpy as np


class Frame:

    def __init__(self, data: np.ndarray):
        self.__frame_data = data

    def GetData(self) -> np.ndarray:
        return self.__frame_data
