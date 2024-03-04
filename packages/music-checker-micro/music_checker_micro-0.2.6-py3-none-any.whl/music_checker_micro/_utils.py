"""
Util repository
"""
import hashlib


def __encode_md5(string: str) -> str:
    """Converts a string into its MD5 representation string"""
    return hashlib.md5(string.encode()).hexdigest()
