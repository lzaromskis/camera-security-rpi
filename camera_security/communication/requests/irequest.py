# irequest.py | camera-security-rpi
# Describes the IRequest interface for client requests
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from camera_security.communication.serializers.packetdataserializer import PacketData
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.responses.idefaultresponses import IDefaultResponses


class IRequest(ABC):

    @abstractmethod
    def Execute(self, data: PacketData,
                authentication_facade: AuthenticationFacade,
                default_responses: IDefaultResponses) -> PacketData:
        """
        Executes the client request
        """
        raise NotImplementedError()
