# requestwithoutauthentication.py | camera-security-rpi
# Inherits the RequestTemplate class and implements the Authenticate method
# Author: Lukas Žaromskis

from abc import ABC
from typing import Tuple, Optional
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requesttemplate import RequestTemplate
from camera_security.communication.responses.idefaultresponses import IDefaultResponses


class RequestWithoutAuthentication(RequestTemplate, ABC):

    def _Authenticate(self, data: PacketData, auth_facade: AuthenticationFacade,
                      default_responses: IDefaultResponses) -> Tuple[bool, Optional[PacketData]]:
        return True, None
