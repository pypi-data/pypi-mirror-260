"""
quickmq.utils
~~~~~~~~~~~~~

Useful functions for quickmq, currently just message encoding/decoding.
"""

import json
from typing import Dict, List, Union

from typing_extensions import TypeAlias

from .exceptions import EncodingError

JSON: TypeAlias = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


def encode_message(message: Union[JSON, bytearray, bytes]) -> bytes:
    if isinstance(message, bytes):
        return message
    elif isinstance(message, bytearray):
        return bytes(message)
    try:
        return bytes(json.dumps(message), encoding="utf-8")
    except (UnicodeEncodeError, TypeError) as e:
        raise EncodingError(f"Could not encode message {message}") from e
