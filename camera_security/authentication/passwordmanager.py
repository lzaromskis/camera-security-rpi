# passwordmanager.py | camera-security-rpi
# Implements the IPasswordManager interface with PasswordManager class
# Author: Lukas Žaromskis

from camera_security.authentication.ihash import IHash
from camera_security.authentication.ipasswordio import IPasswordIO
from camera_security.authentication.ipasswordmanager import IPasswordManager
from camera_security.authentication.isecretgenerator import ISecretGenerator
from camera_security.authentication.passworddata import PasswordData


class PasswordManager(IPasswordManager):

    def __init__(self, hash: IHash, password_io: IPasswordIO, secret_generator: ISecretGenerator):
        self.__hash = hash
        self.__password_io = password_io
        self.__secret_generator = secret_generator

    def IsValid(self, password: str) -> bool:
        data = self.__password_io.GetPassword()
        calculated_hash = self.__hash.Hash(password, data.GetSalt())
        return calculated_hash == data.GetHash()

    def ChangePassword(self, new_password: str):
        generated_salt = self.__secret_generator.Generate(16)
        calculated_hash = self.__hash.Hash(new_password, generated_salt)
        self.__password_io.SavePassword(PasswordData(calculated_hash, generated_salt))
