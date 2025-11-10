import base64
import socket
import time

from upss import utils, consts, log
from upss.connection import ConnectionHandler
from upss.models import Types, Package, Status
from upss.security import Crypto, cryptographer


def start(addr: str, port: int, encoding: str, crypto: Crypto, handlers):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    try:
        serv_sock.bind((addr, port))
        serv_sock.listen(10)
        print(f"Listening on {addr}:{port}")

        while True:
            client_sock, client_addr = serv_sock.accept()
            log.i("COMMON HANDLER", f"Connected by {client_addr}")

            initial_data = client_sock.recv(1024)
            if not initial_data:
                client_sock.close()
                continue

            package = utils.generate_package(initial_data.decode(encoding))

            if package.type == Types.SEND:
                server_package = Package(package.path, Types.SEND, {"public_key": crypto.pem_public_key})
                client_sock.sendall(server_package.get_json().encode(encoding))

                key_data = client_sock.recv(1024)
                if not key_data:
                    client_sock.close()
                    continue

                key_package = utils.generate_package(key_data.decode(encoding))

                if key_package.type == Types.SEND:
                    base64_string = key_package.data["key"]
                    key = crypto.decrypt_data(base64.b64decode(base64_string))

                    confirmation_package = Package(key_package.path, Types.SEND,
                                                   {"msg": cryptographer.encrypt_data(consts.SENTENCE, encoding, key)})
                    client_sock.sendall(confirmation_package.get_json().encode(encoding))

                    status_data = client_sock.recv(1024)
                    if not status_data:
                        client_sock.close()
                        continue

                    status_package = utils.generate_package(status_data.decode(encoding))

                    if status_package.type == Types.STATUS:
                        if status_package.data["status"] == Status.ok:
                            handler_request_data = client_sock.recv(1024)
                            if not handler_request_data:
                                client_sock.close()
                                continue

                            handler_request_package = utils.generate_package(handler_request_data.decode(encoding))

                            access_call = Package(key_package.path, Types.STATUS, {"status": Status.ok})
                            client_sock.sendall(access_call.get_json().encode(encoding))

                            handler_body_data = client_sock.recv(1048576)
                            if not handler_body_data:
                                client_sock.close()
                                continue

                            handler_body_package = utils.generate_package(handler_body_data.decode(encoding))

                            requested_path = handler_request_package.path

                            if requested_path in handlers:
                                handler_func = handlers[requested_path]
                                try:
                                    status = handler_func(client=ConnectionHandler(client_sock, encoding),
                                                          encoding=encoding, key=key, data=handler_body_package.data)
                                    answer_package = Package(requested_path, Types.STATUS, {"status": status})
                                    client_sock.sendall(answer_package.get_json().encode(encoding))
                                except Exception as e:
                                    log.e(requested_path, f"Error in handler for path {requested_path}: {e}")
                                    error_package = Package(requested_path, Types.STATUS, {"status": Status.error})
                                    client_sock.sendall(error_package.get_json().encode(encoding))
                            else:
                                log.e(requested_path, f"No handler found for path: {requested_path}")
                                error_package = Package(requested_path, Types.STATUS, {"status": Status.error})
                                client_sock.sendall(error_package.get_json().encode(encoding))

                        elif package.data["status"] == Status.error:
                            log.e("COMMON HANDLER",
                                  f"The encryption key exchange failed with the following error: {Status.error}")
                        else:
                            log.e("COMMON HANDLER",
                                  f"The encryption key exchange failed with the following error: {Status.wrong_format}")
                else:
                    log.e("COMMON HANDLER", f"Expected SEND after public key, got: {key_package.type}")
            else:
                log.e("COMMON HANDLER", f"Expected initial SEND packet, got: {package.type}")

            client_sock.close()

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        serv_sock.close()
