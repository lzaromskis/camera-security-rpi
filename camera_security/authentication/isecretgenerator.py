# isecretgenerator.py | camera-security-rpi
# Describes the ISecretGenerator interface for generating secrets
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod


class ISecretGenerator(ABC):

    @abstractmethod
    def Generate(self, length: int) -> str:
        """
        Generates a secret of given length.
        """
        raise NotImplementedError()
