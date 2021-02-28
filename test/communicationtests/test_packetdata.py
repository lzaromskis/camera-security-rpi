import unittest
from camera_security.communication.packetdata import PacketData


class PacketDataTests(unittest.TestCase):

    def setUp(self):
        self.data = PacketData()
        self.attr_name = "test_attr"
        self.attr_val = "Hello"

    def test_AddAttribute(self):
        # Arrange

        # Act
        self.data.AddAttribute(self.attr_name, self.attr_val)

        # Assert
        self.assertEqual(1, len(self.data.attributes))
        self.assertEqual(self.attr_val, self.data.attributes[self.attr_name])

    def test_GetAttribute_Exists(self):
        # Arrange

        # Act
        self.data.attributes[self.attr_name] = self.attr_val
        result = self.data.GetAttribute(self.attr_name)

        # Assert
        self.assertEqual(self.attr_val, result)

    def test_GetAttribute_DoesNotExist(self):
        # Arrange

        # Act
        result = self.data.GetAttribute(self.attr_name)

        # Assert
        self.assertEqual(None, result)

    def test_IsValid_Valid(self):
        # Arrange
        self.attr_name = "code"
        self.attr_val = "15"

        # Act
        self.data.attributes[self.attr_name] = self.attr_val
        result = self.data.IsValid()

        # Assert
        self.assertEqual(True, result)

    def test_IsValid_InvalidKey(self):
        # Arrange
        self.attr_name = "not_code"
        self.attr_val = "15"

        # Act
        self.data.attributes[self.attr_name] = self.attr_val
        result = self.data.IsValid()

        # Assert
        self.assertEqual(False, result)

    def test_IsValid_InvalidValue(self):
        # Arrange
        self.attr_name = "code"
        self.attr_val = "fifteen"

        # Act
        self.data.attributes[self.attr_name] = self.attr_val
        result = self.data.IsValid()

        # Assert
        self.assertEqual(False, result)
