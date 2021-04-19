# iheatmapstore.py | camera-security-rpi
# Describes the IHeatmapStore interface to store a list of heatmap data
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import List

from camera_security.monitoring.heatmap.heatmapdata import HeatmapData


class IHeatmapStore(ABC):

    @abstractmethod
    def AddData(self, data: HeatmapData):
        """
        Adds heatmap data to the list
        """
        raise NotImplementedError()

    @abstractmethod
    def GetData(self) -> List[HeatmapData]:
        """
        Returns the list of heatmap data
        """
        raise NotImplementedError()

    @abstractmethod
    def GetDataCopy(self) -> List[HeatmapData]:
        """
        Returns a shallow copy of the list
        """
        raise NotImplementedError()
