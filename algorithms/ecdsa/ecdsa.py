import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
import sys


class ECDSA:
    def __init__(self, curve=ec.SECP256K1()):
        self.curve = curve
        self.private_key = None
        self.public_key = None

    def keygen(self):
        try:
            self.private_key = ec.generate_private_key(self.curve)
            self.public_key = self.private_key.public_key()
            return self.private_key, self.public_key
        except Exception as e:
            print(f"FATAL: ECDSA key generation failed: {e}")
            return None, None

    def sign(self, message, private_key):
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        if private_key is None:
            print("Error: Cannot sign with None private key (ECDSA).")
            return None

        try:
            hasher = hashes.Hash(hashes.SHA256())
            hasher.update(message)
            digest = hasher.finalize()

            signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
            return signature
        except Exception as e:
            print(f"Error during ECDSA signing: {e}")
            return None

    def verify(self, message, signature, public_key):
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        if signature is None:
            return False
        if public_key is None:
            print("Error: Cannot verify with None public key (ECDSA).")
            return False

        try:
            hasher = hashes.Hash(hashes.SHA256())
            hasher.update(message)
            digest = hasher.finalize()

            public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:

            return False
        except Exception as e:

            print(f"Error during ECDSA verification: {e}")
            return False
