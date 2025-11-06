import base64
import socket
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from upss import utils, consts
from upss.models import Package, Types, Status
from upss.security import cryptographer


def encrypt(data_str: str, pem_public_key: str):
    public_key = load_pem_public_key(pem_public_key.encode("utf-8"))
    data = data_str.encode("utf-8")
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data


def connect(url_str: str, encoding: str, send_data, key):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    url_format = utils.generate_url(url_str)
    try:
        s.connect((url_format.addr, url_format.port))
        print(f"Connected to {url_str}")

        package = Package(url_format.path, Types.SEND, {"msg": "hello"})
        s.sendall(package.get_json().encode(encoding))
        data = s.recv(1024)
        package = utils.generate_package(data.decode(encoding))
        if package.type == Types.SEND:
            public_key = package.data["public_key"]
            key_enc = encrypt(key.decode(encoding), public_key)
            base64_encoded_data = base64.b64encode(key_enc)
            base64_string = base64_encoded_data.decode(encoding)
            package = Package(url_format.path, Types.SEND, {"key": base64_string})
            s.sendall(package.get_json().encode(encoding))
            data = s.recv(1024)
            package = utils.generate_package(data.decode(encoding))
            if (cryptographer.decrypt_data(package.data["msg"], encoding, key) == consts.SENTENCE) and (
                    package.type == Types.SEND):
                package = Package(url_format.path, Types.STATUS, {"status": Status.ok})
                s.sendall(package.get_json().encode(encoding))
            else:
                package = Package(url_format.path, Types.STATUS, {"status": Status.error})
                s.sendall(package.get_json().encode(encoding))

            handler_request_package = Package(url_format.path, Types.STATUS, {"action": "call_handler"})
            s.sendall(handler_request_package.get_json().encode(encoding))

            data = s.recv(1024)
            package = utils.generate_package(data.decode(encoding))
            if package.type == Types.STATUS and package.data["status"] == Status.error:
                print("Connection to handler failed")

            handler_body_package = Package(url_format.path, Types.STATUS, send_data)
            s.sendall(handler_body_package.get_json().encode(encoding))

            response_data = s.recv(1048576)
            print(response_data.decode(encoding))

            return utils.generate_package(response_data.decode(encoding))
        else:
            print("Key exchange failed at initial SWAP_KEYS step.")
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        s.close()
