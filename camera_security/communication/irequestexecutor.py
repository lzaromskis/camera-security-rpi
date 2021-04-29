# irequestexecutor.py | camera-security-rpi
# Describes the IRequestExecutor interface for executing client requests
# Author: Lukas Žaromskis

from abc import ABC, abstractmethod

<<<<<<< HEAD
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.requests.requesttemplate import RequestTemplate
=======
from camera_security.communication.requests.irequest import IRequest
from camera_security.communication.requests.requestcode import RequestCode
>>>>>>> main


class IRequestExecutor(ABC):

    @abstractmethod
    def ExecuteRequest(self, data: str) -> str:
        """
        Executes the given request
        """
        raise NotImplementedError()

    @abstractmethod
<<<<<<< HEAD
    def RegisterRequest(self, request_code: RequestCode, request: RequestTemplate):
=======
    def RegisterRequest(self, request_code: RequestCode, request: IRequest):
>>>>>>> main
        """
        Registers a new request that can be executed
        """
        raise NotImplementedError()
