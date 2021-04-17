# ialertaction.py | camera-security-rpi
# Describes the IAlertAction interface for executing an action on alert
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IAlertAction(ABC):

    @abstractmethod
    def Execute(self, **kwargs):
        raise NotImplementedError()
