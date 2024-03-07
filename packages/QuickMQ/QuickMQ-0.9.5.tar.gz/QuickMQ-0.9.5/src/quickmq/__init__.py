import logging

from .adapters.pika import PikaConnection as Connection
from .client import AmqpClient
from .config import ConnectionConfig

__author__ = "Max Drexler"
__email__ = "mndrexler@wisc.edu"
__version__ = "0.9.5"

__all__ = [
    "__version__",
    "__author__",
    "AmqpClient",
    "ConnectionConfig",
    "Connection",
]

logging.getLogger("quickmq").handlers.clear()
logging.getLogger("quickmq").addHandler(logging.NullHandler())
