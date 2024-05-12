import hashlib


def sha256_encrypt(data) -> str:
    """
    Encrypts data using SHA256 algorithm.
    :param data: The string to be encrypted.
    :return: A Hex-digest of the SHA-256 hash of data.
    """
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


def checker(data, digest) -> Bool:
    """
    Checks if the given data has the given SHA-256 hash.
    :param data: The data to be checked.
    :param digest: The digest to be compared to.
    :return: True if the data has the given SHA-256 hash, False otherwise.
    """
    return sha256_encrypt(data) == digest

