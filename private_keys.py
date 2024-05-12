from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class PrivateKey:
    @property
    def alice(self):
        with open("private_key_alice.pem", "rb") as f:
            private_key_pem = f.read()
            return serialization.load_pem_private_key(
                private_key_pem,
                password=None,  # No password
                backend=default_backend()
            )

    @property
    def bob(self):
        with open("private_key_bob.pem", "rb") as f:
            private_key_pem = f.read()
            return serialization.load_pem_private_key(
                private_key_pem,
                password=None,  # No password
                backend=default_backend()
            )

    @property
    def charlie(self):
        with open("private_key_charlie.pem", "rb") as f:
            private_key_pem = f.read()
            return serialization.load_pem_private_key(
                private_key_pem,
                password=None,  # No password
                backend=default_backend()
            )