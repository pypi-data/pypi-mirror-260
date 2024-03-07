"""
easymq.exceptions
~~~~~~~~~~~~~~~~~

Stores all custom exceptions raised in EasyMQ.
"""


class NotAuthenticatedError(ConnectionError):
    """User not authenticated to connect to server"""


class EncodingError(Exception):
    """Error when encoding a message"""


class WrongStateError(Exception):
    """Error when a connection is in the wrong state to perform an action"""


class PublishError(ConnectionError):
    """Error when a publish from a connection fails"""


# Warnings


class UndeliveredWarning(Warning):
    """A message was not delivered to a server"""
