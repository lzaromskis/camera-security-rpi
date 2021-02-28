# loginrequest.py | camera-security-rpi
# Implements the IRequest interface for logging in
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.irequest import IRequest
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode


class LoginRequest(IRequest):

    def Execute(self, data: PacketData,
                authentication_facade: AuthenticationFacade,
                default_responses: IDefaultResponses) -> PacketData:
        password = data.GetAttribute(PacketAttribute.PASSWORD)
        if password is None:
            return default_responses.GetInvalidPacketResponse(PacketAttribute.PASSWORD)
        secret = authentication_facade.Authenticate(password)
        if secret is None:
            ret_val = PacketData()
            ret_val.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_PASSWORD.value))
            ret_val.AddAttribute(PacketAttribute.MESSAGE, "The password you have entered is incorrect.")
            return ret_val
        ret_val = PacketData()
        ret_val.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        ret_val.AddAttribute(PacketAttribute.SECRET, secret)
        ret_val.AddAttribute(PacketAttribute.MESSAGE, "Login successful.")
        return ret_val
