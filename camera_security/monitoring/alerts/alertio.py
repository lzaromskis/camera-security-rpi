# alertio.py | camera-security-rpi
# Describes the AlertIO class implementing the IAlertIO interface
# Author: Lukas Žaromskis

import numpy as np
from os import path, listdir, remove
from typing import List
from camera_security.image.frame import Frame
from camera_security.monitoring.alerts.alertdata import AlertData
from camera_security.monitoring.alerts.ialertio import IAlertIO
from camera_security.utility.exceptions.filenotfounderror import FileNotFoundError


class AlertIO(IAlertIO):

    def __init__(self, alerts_folder="./testalerts/", alerts_to_keep=10):
        self.__alerts_folder = alerts_folder
        self.__alerts_to_keep = alerts_to_keep

    def SaveAlert(self, alert: AlertData):
        data = alert.GetImage().GetData()
        time = alert.GetTimestamp()
        file_path = self.__alerts_folder + time
        # Do not save a file with the same name
        if not path.isfile(file_path):
            with open(file_path, 'wb') as f:
                np.save(f, data)
            self.__CullAlertsFolder()

    def GetAlert(self, timestamp: str) -> AlertData:
        file_path = self.__alerts_folder + timestamp
        if not path.isfile(file_path):
            raise FileNotFoundError("File \"" + file_path + "\" does not exist!")
        with open(file_path, 'rb') as f:
            data = np.load(f)
        return AlertData(timestamp, Frame(data))

    def GetAvailableAlerts(self) -> List[str]:
        return listdir(self.__alerts_folder)

    def __CullAlertsFolder(self):
        files = self.GetAvailableAlerts()
        files.sort()
        count = len(files)
        index = 0
        while count > self.__alerts_to_keep:
            remove(self.__alerts_folder + files[index])
            index = index + 1
            count = count - 1
