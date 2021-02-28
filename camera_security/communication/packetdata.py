# packetdata.py | camera-security-rpi
# Describes the packet data class
# Author: Lukas Žaromskis


class PacketData:

    def __init__(self):
        self.attributes = dict()

    def AddAttribute(self, attribute_name, attribute_data):
        self.attributes[attribute_name] = attribute_data

    def GetAttribute(self, attribute_name):
        try:
            return self.attributes[attribute_name]
        except KeyError:
            return None

    def IsValid(self):
        return "code" in self.attributes.keys() and self.attributes["code"].isdigit()
