# packetdataserializer.py | camera-security-rpi
# Implements the IPacketDataSerializer interface
# Author: Lukas Žaromskis

from camera_security.communication.ipacketdataserializer import IPacketDataSerializer
from camera_security.communication.packetdata import PacketData
from io import StringIO


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
            string_io.write(key)
            string_io.write(self.KEY_VALUE_SEPARATOR)
            string_io.write(value)
            string_io.write(self.PAIR_SEPARATOR)
        string_data = string_io.getvalue()
        string_io.close()
        return string_data

    def Deserialize(self, data: str) -> PacketData:
        if type(data) != str:
            raise TypeError("Data must be a string!")
        packet_data = PacketData()
        split_data = data.split(self.PAIR_SEPARATOR)
        for d in split_data:
            key_value_pair = d.split(self.KEY_VALUE_SEPARATOR)
            # skip if the key value pair is invalid
            if len(key_value_pair) != 2:
                continue
            packet_data.AddAttribute(key_value_pair[0], key_value_pair[1])
        return packet_data
