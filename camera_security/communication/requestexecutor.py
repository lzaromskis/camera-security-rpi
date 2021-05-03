# requestexecutor.py | camera-security-rpi
# Implements the IRequestExecutor interface
# Author: Lukas Žaromskis
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.irequestexecutor import IRequestExecutor
from camera_security.communication.packetattribute import PacketAttribute
from camera_security.communication.packetdata import PacketData
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.requests.requesttemplate import RequestTemplate
from camera_security.communication.responses.idefaultresponses import IDefaultResponses
from camera_security.communication.responses.responsecode import ResponseCode
from camera_security.communication.serializers.ipacketdataserializer import IPacketDataSerializer
from camera_security.utility.exceptions.requestnotfounderror import RequestNotFoundError


class RequestExecutor(IRequestExecutor):

    def __init__(self, packet_data_serializer: IPacketDataSerializer,
                 authentication_facade: AuthenticationFacade,
                 default_responses: IDefaultResponses):
        self.__packet_data_serializer = packet_data_serializer
        self.__authentication_facade = authentication_facade
        self.__default_responses = default_responses
        self.__requests = dict()

    def ExecuteRequest(self, data: str) -> str:
        packet_data = self.__packet_data_serializer.Deserialize(data)
        if not packet_data.IsValid():
            return self.__packet_data_serializer.Serialize(self.__default_responses.GetInvalidPacketResponse())
        code = int(packet_data.GetAttribute(PacketAttribute.CODE))
        try:
            response = self.__requests[code].Execute(packet_data, self.__authentication_facade, self.__default_responses)
            return self.__packet_data_serializer.Serialize(response)
        except KeyError:
            response = self.__default_responses.GetInvalidRequestResponse(code)
            raise RequestNotFoundError("Request not found with code: " + str(code),
                                       self.__packet_data_serializer.Serialize(response))
        except:
            packet = PacketData()
            packet.AddAttribute(PacketAttribute.CODE, str(ResponseCode.SERVER_ERROR.value))
            packet.AddAttribute(PacketAttribute.MESSAGE, "Internal server error")
            return self.__packet_data_serializer.Serialize(packet)

    def RegisterRequest(self, request_code: RequestCode, request: RequestTemplate):
        self.__requests[request_code.value] = request
