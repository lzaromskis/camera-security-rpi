# irequestexecutor.py | camera-security-rpi
# Describes the IRequestExecutor interface for executing client requests
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

from camera_security.communication.requests.irequest import IRequest
from camera_security.communication.requests.requestcode import RequestCode


class IRequestExecutor(ABC):

    @abstractmethod
    def ExecuteRequest(self, data: str) -> str:
        """
        Executes the given request
        """
        raise NotImplementedError()

    @abstractmethod
    def RegisterRequest(self, request_code: RequestCode, request: IRequest):
        """
        Registers a new request that can be executed
        """
        raise NotImplementedError()
