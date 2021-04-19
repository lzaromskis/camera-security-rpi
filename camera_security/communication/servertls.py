# servertls.py | camera-security-rpi
# Implements the IServer interface with TLS security
# Author: Lukas Žaromskis

from camera_security.communication.iserver import IServer
from camera_security.communication.irequestexecutor import IRequestExecutor
from camera_security.utility.exceptions.requestnotfounderror import RequestNotFoundError
from camera_security.utility.ilogger import ILogger
import socket
import threading
import ssl

from camera_security.utility.loglevel import LogLevel


class ServerTLS(IServer):

    def __init__(self, host: str, port: int, cert_file: str, key_file: str,
                 request_executor: IRequestExecutor, logger: ILogger):
        self.__host = host
        self.__port = port
        self.__cert_file = cert_file
        self.__key_file = key_file
        self.__request_executor = request_executor
        self.__logger = logger
        self.__sock = None
        self.__thread = None
        self.__running = False
        self.__context = None

    def StartListening(self):
        self.__thread = threading.Thread(target=self.__StartListeningTask)
        # Set thread as daemon so it closes with the main thread
        self.__thread.daemon = True
        self.__thread.start()

    def IsRunning(self):
        return self.__running

    def __StartListeningTask(self):
        self.__context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.__context.load_cert_chain(self.__cert_file, self.__key_file)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()
        self.__running = True
        self.__logger.Log("Opening socket " + str(self.__host) + ":" + str(self.__port))
        tls_sock = self.__context.wrap_socket(self.__sock, server_side=True)
        while self.__running:
            self.__logger.Log("Accepting connection...")
            try:
                connection, client_address = tls_sock.accept()
                try:
                    self.__logger.Log("Received connection from " + str(client_address))
                    data = connection.recv(1024)
                    if data:
                        str_data = data.decode()
                        try:
                            response = self.__request_executor.ExecuteRequest(str_data)
                        except RequestNotFoundError as e:
                            self.__logger.Log(e.message)
                            response = e.response
                        self.__logger.Log("Sending data to " + str(client_address))
                        size = len(response)
                        self.__logger.Log("Response size: " + str(size) + " B (" + str(size / 1024) + " KB)")
                        connection.sendall(str.encode(''.join(["{:08d}".format(size), response])))
                finally:
                    connection.close()
            except ssl.SSLError as err:
                self.__logger.Log("SSL error raised: " + str(err.args), LogLevel.ERROR)
