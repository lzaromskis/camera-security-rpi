import ssl
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import socket


class ConnectionServer(TCPServer):

    def __init__(self,
                 server_address,
                 request_handler_class,
                 certfile,
                 keyfile,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, request_handler_class, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def GetRequest(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                     server_side=True,
                                     certfile=self.certfile,
                                     keyfile=self.keyfile,
                                     ssl_version=self.ssl_version)
        return connstream, fromaddr


class MySSLThreadingTCPServer(ThreadingMixIn, ConnectionServer): pass


class TestHandler(StreamRequestHandler):
    def handle(self):
        data = self.connection.recv(4096)
        self.wfile.write(data)


print("Starting server...")
MySSLThreadingTCPServer(('127.0.0.1', 5151), TestHandler, "./cert.pem", "./key.pem").serve_forever(0.1)