# idefaultresponses.py | camera-security-rpi
# Contains the interface for default responses to common request actions
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestcode import RequestCode


class IDefaultResponses(ABC):

    @abstractmethod
    def GetInvalidPacketResponse(self) -> PacketData:
        """
        Returns a response packet when the request packet is invalid.
        """
        raise NotImplementedError()

    @abstractmethod
    def GetAuthenticationFailureResponse(self) -> PacketData:
        """
        Returns a response packet when the client failed to authenticate.
        """
        raise NotImplementedError()

    @abstractmethod
    def GetInvalidAttributeInPacketResponse(self, attribute: str) -> PacketData:
        """
        Returns a response packet when the given attribute is invalid.
        """
        raise NotImplementedError()

    @abstractmethod
    def GetInvalidRequestResponse(self, code: int) -> PacketData:
        """
        Returns a response packet when the given request code is invalid
        """
        raise NotImplementedError()
