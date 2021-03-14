# requestwithauthentication.py | camera-security-rpi
# Inherits the RequestTemplate class and implements the Authenticate method
# Author: Lukas Žaromskis

from abc import ABC
from typing import Tuple, Optional
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requesttemplate import RequestTemplate
from camera_security.communication.responses.idefaultresponses import IDefaultResponses


class RequestWithAuthentication(RequestTemplate, ABC):

    def _Authenticate(self, data: PacketData, auth_facade: AuthenticationFacade,
                      default_responses: IDefaultResponses) -> Tuple[bool, Optional[PacketData]]:
        secret = data.GetAttribute(PacketAttribute.SECRET)
        if secret is None:
            return False, default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.SECRET)
        is_authenticated = auth_facade.IsAuthenticated(secret)
        if not is_authenticated:
            return False, default_responses.GetAuthenticationFailureResponse()
        return True, None
