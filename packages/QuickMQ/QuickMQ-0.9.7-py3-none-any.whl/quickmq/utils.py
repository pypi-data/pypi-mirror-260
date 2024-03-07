"""
quickmq.utils
~~~~~~~~~~~~~

Useful functions for quickmq, currently just message encoding/decoding.
"""

import json

from .exceptions import EncodingError


def encode_message(message) -> bytes:
    if isinstance(message, bytes):
        return message
    elif isinstance(message, bytearray):
        return bytes(message)
    try:
        return bytes(json.dumps(message), encoding="utf-8")
    except (UnicodeEncodeError, TypeError) as e:
        raise EncodingError(f"Could not encode message {message}") from e
