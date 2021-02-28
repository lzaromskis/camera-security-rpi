# passworddata.py | camera-security-rpi
# Implements the class for storing password data: hash and salt
# Author: Lukas Žaromskis

class PasswordData:
    def __init__(self, hash, salt):
        self.hash = hash
        self.salt = salt

    def GetHash(self):
        return self.hash

    def GetSalt(self):
        return self.salt
