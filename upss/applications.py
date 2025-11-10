from upss import server, log, consts
from upss.security import Crypto, cryptographer


class UPSS:
    def __init__(self,
                 addr: str = "0.0.0.0",
                 port: int = 8080,
                 encoding: str = "utf-8",
                 crypto: Crypto = cryptographer.generate_crypto(),
                 title: str = "UPSS API",
                 description: str = "Better API for network"
                 ):
        self.addr = addr
        self.port = port
        self.encoding = encoding
        self.crypto = crypto
        self.title = title
        self.description = description
        self.doit = {}

    def url(self, path: str):
        def decorator(function):
            if path in self.doit:
                log.w(path, "is already registered. Overwriting.")
            self.doit[path] = function
            return function
        return decorator

    def run(self):
        print(consts.ASCII)
        print('Server is running on', self.addr, ':', self.port)
        server.start(self.addr, self.port, self.encoding, self.crypto, self.doit)
