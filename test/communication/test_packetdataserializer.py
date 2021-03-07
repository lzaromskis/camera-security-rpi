import unittest
from camera_security.communication.packetdata import PacketData
from camera_security.communication.packetdataserializer import PacketDataSerializer


class PacketDataSerializerTests(unittest.TestCase):

    def setUp(self):
        self.serializer = PacketDataSerializer()
        self.attributes = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }

    def test_Serialize(self):
        # Arrange
        data = PacketData()
        data.attributes = self.attributes
        expected = "key1=value1;key2=value2;key3=value3;"

        # Act
        result = self.serializer.Serialize(data)

        # Assert
        self.assertEqual(expected, result)

    def test_Deserialize(self):
        # Arrange
        data = "key1=value1;key2=value2;key3=value3;"
        expected = self.attributes

        # Act
        result = self.serializer.Deserialize(data)

        # Assert
        self.assertEqual(3, len(result.attributes))
        for k, v in result.attributes.items():
            self.assertEqual(expected[k], v)


if __name__ == '__main__':
    unittest.main()
