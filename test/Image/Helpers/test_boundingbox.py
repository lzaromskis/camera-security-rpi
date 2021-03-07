import unittest
from camera_security.Image.helpers.boundingbox import BoundingBox


class BoundingBoxTests(unittest.TestCase):

    def test_IsColliding_True1(self):
        # Arrange
        a = BoundingBox(2, 2, 5, 4)
        b = BoundingBox(1, 1, 3, 3)

        # Act
        result = a.IsColliding(b)

        # Assert
        self.assertTrue(result)

    def test_IsColliding_True2(self):
        # Arrange
        a = BoundingBox(2, 2, 5, 4)
        b = BoundingBox(4, 1, 6, 3)

        # Act
        result = a.IsColliding(b)

        # Assert
        self.assertTrue(result)

    def test_IsColliding_True3(self):
        # Arrange
        a = BoundingBox(2, 2, 5, 4)
        b = BoundingBox(1, 3, 3, 5)

        # Act
        result = a.IsColliding(b)

        # Assert
        self.assertTrue(result)

    def test_IsColliding_True4(self):
        # Arrange
        a = BoundingBox(2, 2, 5, 4)
        b = BoundingBox(4, 3, 6, 5)

        # Act
        result = a.IsColliding(b)

        # Assert
        self.assertTrue(result)

    def test_IsColliding_False(self):
        # Arrange
        a = BoundingBox(2, 2, 4, 4)
        b = BoundingBox(5, 5, 7, 7)

        # Act
        result = a.IsColliding(b)

        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
