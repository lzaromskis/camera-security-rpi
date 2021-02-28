# idefaultresponses.py | camera-security-rpi
# Contains the interface for default responses to common request actions
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.communication.packetdata import PacketData


class IDefaultResponses(ABC):

    @abstractmethod
    def GetAuthenticationFailureResponse(self) -> PacketData:
        raise NotImplementedError()

    @abstractmethod
    def GetInvalidPacketResponse(self, attribute: str) -> PacketData:
        raise NotImplementedError()

    @abstractmethod
    def GetInvalidRequestResponse(self, code: int) -> PacketData:
        raise NotImplementedError()