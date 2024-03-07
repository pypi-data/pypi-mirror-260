"""
quickmq.api
~~~~~~~~~~

Contains exposed AmqpClient for ease of use.
"""

import atexit
from typing import Optional

from .client import AmqpClient
from .config import ConnectionConfig

_CURRENT_CLIENT: AmqpClient = AmqpClient()


atexit.register(_CURRENT_CLIENT.disconnect)


connect = _CURRENT_CLIENT.connect

disconnect = _CURRENT_CLIENT.disconnect

publish = _CURRENT_CLIENT.publish


def configure(
    DEFAULT_USER: Optional[str] = None,
    DEFAULT_PASS: Optional[str] = None,
    RABBITMQ_PORT: Optional[int] = None,
    VIRTUAL_HOST: Optional[str] = None,
    DEFAULT_EXCHANGE: Optional[str] = None,
    DEFAULT_ROUTE_KEY: Optional[str] = None,
    RECONNECT_TRIES: Optional[int] = None,
    RECONNECT_DELAY: Optional[float] = None,
    DROP_WHILE_RECONNECT: Optional[bool] = None,
) -> ConnectionConfig:
    # Small hack to not re-type all the variables ;)
    return ConnectionConfig(**locals())
