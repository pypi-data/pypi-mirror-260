import hashlib
import hmac
from typing import Optional


def encode_hmac_sha256(secret_key: bytes, message: bytes) -> Optional[bytes]:
    if secret_key is None or message is None:
        return None
    return hmac.new(secret_key, message, hashlib.sha256).digest()


if __name__ == '__main__':
    pass
