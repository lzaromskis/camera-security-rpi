# stringlistserializer.py | camera-security-rpi
# Implements the IStringListSerializer interface for serializing string lists
# Author: Lukas Žaromskis

from io import StringIO
from typing import List

from camera_security.utility.serializers.istringlistserializer import IStringListSerializer


class StringListSerializer(IStringListSerializer):

    ITEM_SEPARATOR = ','

    def Serialize(self, data: List[str]) -> str:
        string_io = StringIO()
        for d in data[:-1]:
            if self.ITEM_SEPARATOR not in d:
                string_io.write(d)
                string_io.write(self.ITEM_SEPARATOR)
        item = data[-1]
        if self.ITEM_SEPARATOR not in item:
            string_io.write(item)
        string_data = string_io.getvalue()
        string_io.close()
        return string_data

    def Deserialize(self, data: str) -> List[str]:
        return data.split(self.ITEM_SEPARATOR)

