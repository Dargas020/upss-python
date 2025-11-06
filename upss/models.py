import json

from upss import consts
from upss.exception import URLError


class Package:
    def __init__(self, path: str, type: str, data):
        self.path = path
        self.type = type
        self.data = data

    def __str__(self):
        return "{" + f"'meta': '{consts.META}', 'path': '{self.path}', 'type': '{self.type}', 'data': {self.data}" + "}"

    def get_obj(self):
        return {
            "meta": consts.META,
            "path": self.path,
            "type": self.type,
            "data": self.data
        }

    def get_json(self):
        return json.dumps(self.get_obj())


class URL:
    def __init__(self, protocol: str, addr: str, port: int, path: str):
        if protocol != consts.PROTOCOL:
            raise URLError("The protocol specified is incorrect. Only 'upss' is supported")
        if path[0] != "/":
            raise URLError("The path must start with the '/' character")
        self.protocol = protocol
        self.addr = addr
        self.port = port
        self.path = path

    def __str__(self):
        return f"protocol: {self.protocol}, addr: {self.addr}, port: {self.port}, path: {self.path}"


class Types:
    SEND = "SEND"
    STATUS = "STATUS"


class Status:
    ok = "OK"
    error = "ERROR"
    wrong_format = "WRONG_FORMAT"
