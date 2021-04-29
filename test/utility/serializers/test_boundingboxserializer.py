import unittest

from camera_security.utility.boundingbox import BoundingBox
from camera_security.utility.exceptions.deserializationfailederror import DeserializationFailedError
from camera_security.utility.serializers.boundingboxserializer import BoundingBoxSerializer


class BoundingBoxSerializerTests(unittest.TestCase):
    def test_serialize(self):
        # Arrange
        expected = "1,2,3,4"
        box = BoundingBox(1, 2, 3, 4)
        serializer = BoundingBoxSerializer()

        # Act
        result = serializer.Serialize(box)

        # Assert
        self.assertEqual(result, expected)

    def test_deserialize_successful(self):
        # Arrange
        data = "1,2,3,4"
        expected = BoundingBox(1, 2, 3, 4)
        serializer = BoundingBoxSerializer()

        # Act
        result = serializer.Deserialize(data)

        # Assert
        self.assertEqual(result, expected)

    def test_deserializer_raises_exception(self):
        # Arrange
        data = "1, 4"
        serializer = BoundingBoxSerializer()

        # Act
        # Assert
        with self.assertRaises(DeserializationFailedError) as error:
            serializer.Deserialize(data)
        self.assertEqual("Failed to deserialize the given string to a bounding box", error.exception.message)


if __name__ == '__main__':
    unittest.main()
