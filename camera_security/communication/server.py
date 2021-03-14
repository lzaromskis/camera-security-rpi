# server.py | camera-security-rpi
# Implements the IServer interface
# Author: Lukas Žaromskis

from camera_security.communication.iserver import IServer
from camera_security.communication.irequestexecutor import IRequestExecutor
from camera_security.exceptions import RequestNotFoundError
from camera_security.utility.ilogger import ILogger
import socket
import threading


class Server(IServer):

    def __init__(self, host: str, port: int, request_executor: IRequestExecutor, logger: ILogger):
        self.__host = host
        self.__port = port
        self.__request_executor = request_executor
        self.__logger = logger
        self.__sock = None
        self.__thread = None
        self.__running = False

    def StartListening(self):
        self.__thread = threading.Thread(target=self.__StartListeningTask)
        # Set thread as daemon so it closes with the main thread
        self.__thread.daemon = True
        self.__thread.start()

    def IsRunning(self):
        return self.__running

    def __StartListeningTask(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()
        self.__running = True
        self.__logger.Log("Opening socket " + str(self.__host) + ":" + str(self.__port))
        while self.__running:
            self.__logger.Log("Accepting connection...")
            connection, client_address = self.__sock.accept()
            try:
                self.__logger.Log("Received connection from " + str(client_address))
                data = connection.recv(1024)
                if data:
                    str_data = data.decode()
                    self.__logger.Log("Received message: " + str_data)
                    try:
                        response = self.__request_executor.ExecuteRequest(str_data)
                    except RequestNotFoundError as e:
                        self.__logger.Log(e.message)
                        response = e.response
                    self.__logger.Log("Sending data to " + str(client_address))
                    size = len(response)
                    self.__logger.Log("Response size: " + str(size) + " B (" + str(size / 1024) + " KB)")
                    connection.sendall(str.encode(response))
            finally:
                connection.close()


# class Server(IServer):
#
#     __request_executor = None
#
#     def __init__(self, host, port, request_executor):
#         self.host = host
#         self.port = port
#         self.is_running = False
#         self.server = None
#         self.coroutine = None
#         self.loop = None
#         self.thread = None
#         Server.__request_executor = request_executor
#
#     def StartListening(self):
#         self.loop = asyncio.get_event_loop()
#         self.coroutine = asyncio.start_server(Server.ConnectionCallback, self.host, self.port, loop=self.loop)
#         self.server = self.loop.run_until_complete(self.coroutine)
#         self.thread = threading.Thread(target=self.loop.run_forever)
#         # Set thread as daemon so it closes with the main thread
#         self.thread.daemon = True
#         self.thread.start()
#
#     @staticmethod
#     async def ConnectionCallback(reader, writer):
#         print("Connected!")
#         data = await reader.read(1024)
#         str_data = data.decode()
#         print("Received: " + str_data)
#         response = Server.__request_executor.ExecuteRequest(str_data)
#         writer.write(str.encode(response))
#         await writer.drain()
#         writer.close()

import time
from camera_security.utility.consolelogger import ConsoleLogger
from camera_security.communication.requestexecutor import RequestExecutor
from camera_security.communication.packetdataserializer import PacketDataSerializer
from camera_security.communication.responses.defaultresponses import DefaultResponses
from camera_security.authentication.authenticationfacade import AuthenticationFacade
from camera_security.communication.requests.requestcode import RequestCode
from camera_security.communication.requests.loginrequest import LoginRequest
from camera_security.communication.requests.changepasswordrequest import ChangePasswordRequest
from camera_security.communication.requests.getimagerequest import GetImageRequest
from camera_security.authentication.mockauthenticationfacade import MockAuthenticationFacade
from camera_security.communication.servertls import ServerTLS
from camera_security.image.imagefacade import ImageFacade
from camera_security.image.helpers.bmpbase64frameserializer import BmpBase64FrameSerializer
from camera_security.image.helpers.jpgbase64frameserializer import JpgBase64FrameSerializer
executor = RequestExecutor(PacketDataSerializer(), MockAuthenticationFacade(), DefaultResponses())
executor.RegisterRequest(RequestCode.LOGIN, LoginRequest())
executor.RegisterRequest(RequestCode.CHANGE_PASSWORD, ChangePasswordRequest())
executor.RegisterRequest(RequestCode.GET_IMAGE, GetImageRequest(ImageFacade(), JpgBase64FrameSerializer()))
s = Server("127.0.0.1", 7500, executor, ConsoleLogger())
# s = ServerTLS("127.0.0.1", 7500, "cert.pem", "key.pem", executor, ConsoleLogger())
s.StartListening()
print("Exited StartListening()")
print("Sleeping for 1000 seconds...")
time.sleep(1000)
print("Woke up. Shutting down the server...")
