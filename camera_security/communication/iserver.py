# iserver.py | camera-security-rpi
# Describes the IServer interface
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class IServer(ABC):

    @abstractmethod
    def StartListening(self):
        """
        Starts listening on a server socket
        """
        raise NotImplementedError()

    @abstractmethod
    def IsRunning(self) -> bool:
        """
        Returns True if the server is running
        """
        raise NotImplementedError()
