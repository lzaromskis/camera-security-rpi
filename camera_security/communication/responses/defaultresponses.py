# defaultresponses.py | camera-security-rpi
# Implements the IDefaultResponses interface for default responses to common request actions
# Author: Lukas Žaromskis
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.communication.packetattribute import PacketAttribute


class DefaultResponses(IDefaultResponses):

    def GetInvalidPacketResponse(self) -> PacketData:
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.INVALID_PACKET.value))
        packet.AddAttribute(PacketAttribute.MESSAGE,
                            "The received packet is invalid. It may be corrupted.")
        return packet

    def GetAuthenticationFailureResponse(self) -> PacketData:
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.NOT_AUTHENTICATED.value))
        packet.AddAttribute(PacketAttribute.MESSAGE, "You are not authenticated.")
        return packet

    def GetInvalidAttributeInPacketResponse(self, attribute: str) -> PacketData:
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.INVALID_PACKET.value))
        packet.AddAttribute(PacketAttribute.MESSAGE,
                            "The given attribute is either missing or invalid: " + attribute)
        return packet

    def GetInvalidRequestResponse(self, code: int) -> PacketData:
        packet = PacketData()
        packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.INVALID_REQUEST.value))
        packet.AddAttribute(PacketAttribute.MESSAGE,
                            "Received an unknown request with code: " + str(code.value))
        return packet
