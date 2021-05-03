# stringlistserializer.py | camera-security-rpi
# Implements the IStringListSerializer interface for serializing string lists
# Author: Lukas Žaromskis

from io import StringIO
from typing import List

from camera_security.utility.serializers.istringlistserializer import IStringListSerializer


class StringListSerializer(IStringListSerializer):

    ITEM_SEPARATOR = ','

    def Serialize(self, data: List[str]) -> str:
        return self.ITEM_SEPARATOR.join(data)

    def Deserialize(self, data: str) -> List[str]:
        return data.split(self.ITEM_SEPARATOR)

