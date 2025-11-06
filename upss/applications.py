from upss import server
from upss.security import Crypto


class UPSS:
    def __init__(self, addr: str, port: int, encoding: str, crypto: Crypto):
        self.addr = addr
        self.port = port
        self.encoding = encoding
        self.crypto = crypto
        self.doit = {}

    def url(self, path: str):
        def decorator(function):
            if path in self.doit:
                print(f"Warning: Path '{path}' is already registered. Overwriting.")
            self.doit[path] = function
            return function
        return decorator

    def run(self):
        print('Server is running on', self.addr, ':', self.port)
        server.start(self.addr, self.port, self.encoding, self.crypto, self.doit)
