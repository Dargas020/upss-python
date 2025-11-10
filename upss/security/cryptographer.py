import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from upss.security import Crypto


def generate_crypto():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return Crypto(private_key, public_key, pem_public_key)


def encrypt_data(data_str: str, encoding: str, key):
    cipher_suite = Fernet(key)

    data = data_str.encode(encoding)
    encrypted_data = cipher_suite.encrypt(data)

    base64_encoded_data = base64.b64encode(encrypted_data)
    base64_string = base64_encoded_data.decode(encoding)

    return base64_string


def decrypt_data(encrypted_data: str, encoding: str, key):
    cipher_suite = Fernet(key)

    original_byte_array = base64.b64decode(encrypted_data)

    decrypted_data = cipher_suite.decrypt(original_byte_array)

    return decrypted_data.decode(encoding)
