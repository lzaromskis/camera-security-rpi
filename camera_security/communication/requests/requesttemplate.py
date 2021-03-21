# requesttemplate.py | camera-security-rpi
# Describes the RequestTemplate class for defining a template for all requests
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
from typing import Optional, Tuple
from camera_security.communication.serializers.packetdataserializer import PacketData
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.responses.idefaultresponses import IDefaultResponses


class RequestTemplate(ABC):

    def Execute(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        """
        Executes the client request
        """
        is_auth, response = self._Authenticate(data, auth_facade, default_responses)
        if is_auth:
            response = self._ProcessRequest(data, auth_facade, default_responses)
        return response

    @abstractmethod
    def _Authenticate(self, data: PacketData,
                      auth_facade: AuthenticationFacade,
                      default_responses: IDefaultResponses) -> Tuple[bool, Optional[PacketData]]:
        raise NotImplementedError()

    @abstractmethod
    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        raise NotImplementedError()
