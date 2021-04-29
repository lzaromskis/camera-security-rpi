# ialertserver.py | camera-security-rpi
# Describes the IAlertServer interface for alerting the user when a detection happens
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IAlertServer(ABC):

    @abstractmethod
    def StartListening(self):
        raise NotImplementedError()

    @abstractmethod
    def SendMessage(self, message: str):
        raise NotImplementedError()
