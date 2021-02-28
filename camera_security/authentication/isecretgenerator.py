# isecretgenerator.py | camera-security-rpi
# Describes the ISecretGenerator interface for generating secrets
# Implements the interface with SecretGenerator class
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod
import string
import secrets


class ISecretGenerator(ABC):

    @abstractmethod
    def Generate(self, length):
        raise NotImplementedError()


class SecretGenerator(ISecretGenerator):

    def __init__(self):
        pass

    def Generate(self, length):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
