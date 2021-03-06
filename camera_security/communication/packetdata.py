# packetdata.py | camera-security-rpi
# Describes the packet data class
# Author: Lukas Žaromskis

from typing import Optional, Dict
from camera_security.communication.packetattribute import PacketAttribute


class PacketData:

    def __init__(self):
        self.attributes: Dict[str, str] = dict()

    def AddAttribute(self, attribute_name: str, attribute_data: str):
        """
        Adds an attribute to the PacketData dictionary.
        """
        if not attribute_data.strip():
            attribute_data = "NULL"
        self.attributes[attribute_name] = attribute_data

    def GetAttribute(self, attribute_name: str) -> Optional[str]:
        """
        Gets the value of the given attribute. Returns None if attribute does not exist.
        """
        try:
            return self.attributes[attribute_name]
        except KeyError:
            return None

    def IsValid(self) -> bool:
        """
        Checks if the PacketData object is valid.
        """
        return PacketAttribute.CODE in self.attributes.keys() and self.attributes[PacketAttribute.CODE].isdigit()
