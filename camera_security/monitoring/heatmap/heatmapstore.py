# heatmapstore.py | camera-security-rpi
# Implements the IHeatmapStore interface to store a list of heatmap data
# Author: Lukas Žaromskis

from collections import deque
from threading import Lock
from typing import List

from camera_security.monitoring.heatmap.heatmapdata import HeatmapData
from camera_security.monitoring.heatmap.iheatmapstore import IHeatmapStore


class HeatmapStore(IHeatmapStore):

    def __init__(self, time_to_store: float):
        self.__time_to_store = time_to_store
        self.__current_store_time = 0.0
        self.__data_array = deque()
        self.__lock = Lock()

    def AddData(self, data: HeatmapData):
        self.__lock.acquire()
        self.__current_store_time = self.__current_store_time + data.GetTime()
        self.__data_array.append(data)
        if self.__current_store_time > self.__time_to_store:
            popped = self.__data_array.popleft()
            self.__current_store_time = self.__current_store_time - popped.GetTime()
        self.__lock.release()

    def GetData(self) -> List[HeatmapData]:
        self.__lock.acquire()
        ret_data = list(self.__data_array)
        self.__lock.release()
        return ret_data

    def GetDataCopy(self) -> List[HeatmapData]:
        self.__lock.acquire()
        ret_data = list(self.__data_array.copy())
        self.__lock.release()
        return ret_data

    def GetTimeToStore(self):
        return self.__time_to_store
