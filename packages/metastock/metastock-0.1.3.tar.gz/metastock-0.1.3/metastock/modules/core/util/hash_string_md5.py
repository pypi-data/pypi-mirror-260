import hashlib


def hash_string_md5(input_string) -> str:
    hasher = hashlib.md5()
    hasher.update(input_string.encode('utf-8'))
    hashed_string = hasher.hexdigest()
    return hashed_string
