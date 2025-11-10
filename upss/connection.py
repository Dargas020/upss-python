import socket

from upss import utils

from upss.models import Package


class ConnectionHandler:
    def __init__(self, sock: socket, encoding: str):
        self.sock = sock
        self.encoding = encoding

    def send(self, package: Package):
        self.sock.sendall(package.get_json().encode(self.encoding))

    def get(self):
        response_data = self.sock.recv(1048576)
        return utils.generate_package(response_data.decode(self.encoding))
