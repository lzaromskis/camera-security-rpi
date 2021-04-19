# packetdataserializer.py | camera-security-rpi
# Implements the IPacketDataSerializer interface
# Author: Lukas Žaromskis

from camera_security.communication.serializers.ipacketdataserializer import IPacketDataSerializer
from camera_security.communication.packetdata import PacketData
from io import StringIO
from camera_security.utility.exceptions.invalidpacketattributevalueerror import InvalidPacketAttributeValueError


class PacketDataSerializer(IPacketDataSerializer):
    KEY_VALUE_SEPARATOR = '='
    PAIR_SEPARATOR = ';'

    def __init__(self):
        pass

    def Serialize(self, data: PacketData) -> str:
        if type(data) != PacketData:
            raise TypeError("Data must be a PacketData")
        string_io = StringIO()
        for key, value in data.attributes.items():
            if value.find(self.PAIR_SEPARATOR) != -1:
                raise InvalidPacketAttributeValueError(''.join(["Given attribute's '",
                                                                key,
                                                                "' value contains the pair separator character '",
                                                                self.PAIR_SEPARATOR,
                                                                "'"]))
            string_io.write(key)
            string_io.write(self.KEY_VALUE_SEPARATOR)
            string_io.write(value)
            string_io.write(self.PAIR_SEPARATOR)
        string_data = string_io.getvalue()
        string_io.close()
        return string_data

    def Deserialize(self, data: str) -> PacketData:
        if type(data) != str:
            raise TypeError("Data must be a string")
        packet_data = PacketData()
        split_data = data.split(self.PAIR_SEPARATOR)
        for d in split_data:
            length = len(d)
            split_index = d.find(self.KEY_VALUE_SEPARATOR)
            if split_index == -1 or split_index == length - 1:
                continue
            key = d[0: split_index]
            value = d[split_index + 1:]
            packet_data.AddAttribute(key, value)
        return packet_data
