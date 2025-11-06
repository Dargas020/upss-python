from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class Crypto:
    def __init__(self, private_key, public_key, pem_public_key):
        self.private_key = private_key
        self.public_key = public_key
        self.pem_public_key = pem_public_key

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data
