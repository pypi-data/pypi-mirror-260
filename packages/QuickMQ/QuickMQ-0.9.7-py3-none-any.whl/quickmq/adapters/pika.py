import logging
import queue
import socket
import time
from typing import Optional

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.adapters.utils.connection_workflow import AMQPConnectorException
from pika.exceptions import (
    AMQPConnectionError,
    AuthenticationError,
    ChannelClosed,
    ProbableAccessDeniedError,
    ProbableAuthenticationError,
)

from quickmq.abstracts import BaseActor, BaseConnection, ConnectionState
from quickmq.config import ConnectionConfig
from quickmq.exceptions import NotAuthenticatedError, PublishError, WrongStateError

LOGGER = logging.getLogger("quickmq")


class PikaActor(BaseActor["PikaConnection"]):
    def _publish(self, msg: bytes, route_key: str, exchange: str) -> None:
        LOGGER.debug(f"Publishing {msg[:50]!r} to {self._con.destination!r}")
        try:
            self._con._publish_channel.basic_publish(
                body=msg,
                exchange=exchange,
                routing_key=route_key,
                properties=pika.BasicProperties(content_type="application/json"),
            )
        except ChannelClosed as e:
            raise PublishError(
                f"Couldn't publish {msg[:10]!r} to {exchange!r}, route {route_key!r}"
            ) from e
        finally:
            if self._con._publish_channel.is_closed:
                self._con._publish_channel = self._con._server_connection.channel()
                self._con._publish_channel.confirm_delivery()


class PikaConnection(BaseConnection[PikaActor]):
    """Connection adapter using the pika library"""

    def __init__(
        self,
        destination: str,
        usr: str,
        pwd: str,
        *,
        cfg: Optional[ConnectionConfig] = None,
    ) -> None:
        super().__init__(destination, usr, pwd, cfg=cfg)

        self._sleep_interval = 0.5

        # Pika specific connection parameters
        self._actor: Optional[PikaActor] = None
        self._server_connection: pika.BlockingConnection
        self._publish_channel: BlockingChannel
        self._pika_params = pika.ConnectionParameters(
            host=self._dest,
            port=self._config.RABBITMQ_PORT,
            virtual_host=self._config.VIRTUAL_HOST,
            credentials=pika.PlainCredentials(self._usr, self._pwd),
        )

    @property
    def actor(self) -> PikaActor:
        if self._actor is None:
            self._actor = PikaActor(self)
        return self._actor

    def _create_connection(self, tries: int) -> pika.BlockingConnection:
        LOGGER.debug(
            f"Attempting to create connection to {self._dest} with {tries} attempts!"
        )
        _tries = tries
        while _tries:
            if self.state is ConnectionState.DISCONNECTING:
                raise WrongStateError()
            try:
                return pika.BlockingConnection(parameters=self._pika_params)
            except (
                AuthenticationError,
                ProbableAccessDeniedError,
                ProbableAuthenticationError,
            ) as e:
                err_msg = (
                    "Not authenticated to connect to "
                    f"{self._dest}:{self._config.RABBITMQ_PORT}"
                    f"({self._config.VIRTUAL_HOST!r}) with username {self._usr!r}"
                )
                LOGGER.error(err_msg)
                raise NotAuthenticatedError(err_msg) from e
            except (
                socket.gaierror,
                socket.herror,
                AMQPConnectorException,
                AMQPConnectionError,
            ) as e:
                LOGGER.error(f"Attempt {_tries} to connect to {self._dest} failed! {e}")
                _tries -= 1
                if not _tries:
                    raise ConnectionError(
                        f"Couldn't establish {self} after " f"{tries} attempt(s)!"
                    ) from e

            # wait RECONNECT_DELAY, but be aware of calls to disconnect()
            _num_sleeps = int(self._config.RECONNECT_DELAY / self._sleep_interval)
            while self.state is not ConnectionState.DISCONNECTING and _num_sleeps:
                time.sleep(self._sleep_interval)
                _num_sleeps -= 1
        raise ValueError("Tries cannot be 0!")

    def _connect(self) -> None:
        if not hasattr(self, "_server_connection"):
            attmpts = 1  # initial connection attempt
        else:
            attmpts = self._config.RECONNECT_TRIES

        self._server_connection = self._create_connection(attmpts)
        self._publish_channel = self._server_connection.channel()
        self._publish_channel.confirm_delivery()

    def _disconnect(self):
        self._action_queue.join()
        self.join()
        if not hasattr(self, "_server_connection"):
            return
        self._server_connection.process_data_events(1)
        if self._server_connection.is_open:
            self._server_connection.close(0)

    def _run(self) -> None:
        super()._run()
        while self.state is ConnectionState.CONNECTED:
            try:
                self._server_connection.process_data_events(0.005)  # type: ignore [arg-type]
            except (
                AMQPConnectionError,
                ConnectionError,
            ) as e:  # Handle disconnects by broker in the future
                LOGGER.warning(
                    f"Lost connection to {self._dest}! {e} Attempting reconnect"
                )
                self.connect()
                continue
            try:
                next_action, kwargs = self._action_queue.get_nowait()
            except queue.Empty:
                continue
            try:
                self._action_rv = next_action(**kwargs)
            except Exception as e:
                self._action_err = e
            finally:
                self._action_queue.task_done()
