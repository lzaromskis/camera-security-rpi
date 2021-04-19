# passwordmanagerbuilder.py | camera-security-rpi
# Implements the IPasswordManagerFactory interface with PasswordManagerFactory class
# Author: Lukas Žaromskis
from camera_security.authentication.hashsha256 import HashSHA256
from camera_security.authentication.hashsha512 import HashSHA512
from camera_security.authentication.ipasswordmanager import IPasswordManager
from camera_security.authentication.ipasswordmanagerbuilder import IPasswordManagerBuilder
from camera_security.authentication.passwordio import PasswordIO
from camera_security.authentication.passwordmanager import PasswordManager
from camera_security.authentication.secretgenerator import SecretGenerator


class PasswordManagerBuilder(IPasswordManagerBuilder):

    def __init__(self):
        self.__secret_generator_method = ""
        self.__password_io_method = ""
        self.__password_file = ""
        self.__hash_method = ""

    def AddSecretGenerator(self, gen_method: str) -> 'IPasswordManagerBuilder':
        self.__secret_generator_method = gen_method.lower()
        return self

    def AddPasswordIO(self, io_method: str, password_file: str) -> 'IPasswordManagerBuilder':
        self.__password_io_method = io_method.lower()
        self.__password_file = password_file
        return self

    def AddHash(self, hash_method: str) -> 'IPasswordManagerBuilder':
        self.__hash_method = hash_method.lower()
        return self

    def Build(self) -> IPasswordManager:
        # Construct hash
        if self.__hash_method == "sha256":
            hash = HashSHA256()
        elif self.__hash_method == "sha512":
            hash = HashSHA512()
        else:
            hash = HashSHA256()

        # Construct password io
        if self.__password_io_method == "passwordio":
            io = PasswordIO(self.__password_file)
        else:
            io = PasswordIO(self.__password_file)

        # Construct secret generator
        if self.__secret_generator_method == "secretgenerator":
            gen = SecretGenerator()
        else:
            gen = SecretGenerator()

        return PasswordManager(hash, io, gen)
