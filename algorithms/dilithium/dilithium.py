import time
import sys
import oqs


class Dilithium:
    def __init__(self, security_level=3):
        self.security_level = security_level
        self.algorithm_name = f"Dilithium{security_level}"
        self.private_key = None
        self.public_key = None

        try:
            if hasattr(oqs, "get_enabled_sig_mechanisms"):
                sig_mechanisms = oqs.get_enabled_sig_mechanisms()
            elif hasattr(oqs.Signature, "get_supported_sigs"):
                sig_mechanisms = oqs.Signature.get_supported_sigs()
            else:
                print(
                    "Warning: Could not verify supported OQS mechanisms. Proceeding..."
                )
                sig_mechanisms = [self.algorithm_name]

            if self.algorithm_name not in sig_mechanisms:
                print(
                    f"\nERROR: Dilithium algorithm '{self.algorithm_name}' is not enabled in this build."
                )
                print(f"Supported signature algorithms: {sig_mechanisms}")
                sys.exit(f"Exiting: Algorithm {self.algorithm_name} not supported.")
        except AttributeError as e:
            print(
                f"\nWarning: Could not check OQS algorithm status via expected methods ({e}). Proceeding with caution."
            )
        except Exception as e:
            print(
                f"\nERROR checking OQS algorithm status for '{self.algorithm_name}': {e}"
            )
            sys.exit("Exiting: OQS library check failed.")

    def keygen(self):
        try:
            with oqs.Signature(self.algorithm_name) as signer:

                self.public_key = signer.generate_keypair()

                self.private_key = signer.export_secret_key()

            if self.public_key is None or self.private_key is None:
                raise RuntimeError("OQS key generation returned None.")

            return self.private_key, self.public_key
        except Exception as e:
            print(f"FATAL: Dilithium key generation failed: {e}")
            self.private_key = None
            self.public_key = None
            return None, None

    def sign(self, message, private_key_bytes):
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        if private_key_bytes is None:
            print("Error: Cannot sign with None private key (Dilithium).")
            return None

        try:
            with oqs.Signature(self.algorithm_name, private_key_bytes) as signer:
                signature_bytes = signer.sign(message)
            return signature_bytes
        except Exception as e:
            print(f"Error during Dilithium signing: {e}")
            return None

    def verify(self, message, signature_bytes, public_key_bytes):
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        if signature_bytes is None:
            return False
        if public_key_bytes is None:
            print("Error: Cannot verify with None public key (Dilithium).")
            return False

        is_valid = False
        try:
            with oqs.Signature(self.algorithm_name) as verifier:
                is_valid = verifier.verify(message, signature_bytes, public_key_bytes)
        except Exception as e:
            print(f"Error during Dilithium verification: {e}")
            is_valid = False

        return is_valid
