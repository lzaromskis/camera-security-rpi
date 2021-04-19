# changepasswordrequest.py | camera-security-rpi
# Implements the IRequest interface for changing the password
# Author: Lukas Žaromskis

from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestwithauthentication import RequestWithAuthentication
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode


class ChangePasswordRequest(RequestWithAuthentication):

    def _ProcessRequest(self, data: PacketData, auth_facade: AuthenticationFacade, default_responses: IDefaultResponses) -> PacketData:
        password = data.GetAttribute(PacketAttribute.PASSWORD)
        if password is None:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.PASSWORD)
        new_password = data.GetAttribute(PacketAttribute.PASSWORD_NEW)
        if new_password is None:
            return default_responses.GetInvalidAttributeInPacketResponse(PacketAttribute.PASSWORD_NEW)
        is_password_valid = auth_facade.IsPasswordValid(password)
        if not is_password_valid:
            ret_val = PacketData()
            ret_val.AddAttribute(PacketAttribute.CODE, str(ResponseCode.BAD_PASSWORD.value))
            ret_val.AddAttribute(PacketAttribute.MESSAGE, "The password you have entered is incorrect.")
            return ret_val
        auth_facade.ChangePassword(new_password)
        new_secret = auth_facade.Authenticate(new_password)
        ret_val = PacketData()
        ret_val.AddAttribute(PacketAttribute.CODE, str(ResponseCode.OK.value))
        ret_val.AddAttribute(PacketAttribute.MESSAGE, "Password changed successfully.")
        ret_val.AddAttribute(PacketAttribute.SECRET, new_secret)
        return ret_val
