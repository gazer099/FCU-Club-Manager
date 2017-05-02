import hashlib


def get_digest(password):
    return hashlib.sha256(password).hexdigest()


def is_password(password, digest):
    return get_digest(password) == digest
