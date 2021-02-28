import unittest
from camera_security.authentication.ihash import HashSHA256


class HashSHA256Tests(unittest.TestCase):
    def test_hash(self):
        # Arrange
        password_input = "Hello"
        salt_input = " world!"
        expected = "c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a"
        hash_obj = HashSHA256()

        # Act
        result = hash_obj.Hash(password_input, salt_input)

        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
