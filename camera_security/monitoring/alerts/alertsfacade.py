# imagefacade.py | camera-security-rpi
# Describes the AlertsFacade class for controlling the alerts reading and saving subsystem
# Author: Lukas Žaromskis
from datetime import datetime
from typing import List

from camera_security.image.frame import Frame
from camera_security.monitoring.alerts.alertdata import AlertData
from camera_security.monitoring.alerts.alertio import AlertIO


class AlertsFacade:

    def __init__(self, alerts_folder: str, alerts_to_keep: int):
        self.__alert_io = AlertIO(alerts_folder, alerts_to_keep)

    def SaveAlert(self, image: Frame):
        """
        Saves the given frame to a file
        """
        time = datetime.now()
        time_str = time.strftime("%Y-%m-%d_%H-%M-%S_%f")
        data = AlertData(time_str, image)
        self.__alert_io.SaveAlert(data)

    def GetAvailableAlerts(self) -> List[str]:
        """
        Gets the available alerts
        """
        return self.__alert_io.GetAvailableAlerts()

    def GetAlert(self, timestamp: str) -> Frame:
        """
        Gets the given alert's data
        :return:
        """
        return self.__alert_io.GetAlert(timestamp).GetImage()
