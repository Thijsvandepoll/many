import hashlib


def create_hash(s: str):
    return hashlib.shake_256(s.encode()).hexdigest(5)
