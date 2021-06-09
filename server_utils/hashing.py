from hashlib import sha3_224

def hash_pw(to_hash: bytes, length: int) -> bytes:
    sha = sha3_224(to_hash)
    return sha.hexdigest().encode()[:length]
