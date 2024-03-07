"""
quickmq.client
~~~~~~~~~~~~~~

This module contains the main client class.
"""

import logging
from collections import namedtuple
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from .abstracts import BaseConnection, ConnectionState
from .adapters.pika import PikaConnection
from .config import ConnectionConfig

LOGGER = logging.getLogger("quickmq")

D = TypeVar("D")


class NotSet:
    def __repr__(self) -> str:
        return "<NOT SET>"


class MatchAny:
    def __eq__(self, __value: object) -> bool:
        return True

    def __repr__(self) -> str:
        return "<ANY>"


NOTSET = NotSet()
MATCHANY = MatchAny()

connection_id = namedtuple("connection_id", ["destination", "port", "vhost", "user"])


class AmqpClient:
    def __init__(self, con_class: Optional[BaseConnection] = None) -> None:
        self._con_cls: Type[BaseConnection] = con_class or PikaConnection
        # Identify unique connections by server, port, vhost, and user.
        self._connection_pool: Dict[connection_id, BaseConnection] = {}

    @property
    def num_connections(self) -> int:
        return len(self._connection_pool)

    @property
    def connection_ids(self) -> List[connection_id]:
        return list(self._connection_pool.keys())

    def get_connections_where(
        self,
        destination: Optional[str] = None,
        port: Optional[int] = None,
        vhost: Optional[str] = None,
        user: Optional[str] = None,
        default=NOTSET,
    ) -> List[BaseConnection]:
        if destination is None and port is None and vhost is None and user is None:
            raise ValueError("Must specify at least one identifier!")

        match_tuple = connection_id(
            destination or MATCHANY,
            port or MATCHANY,
            vhost or MATCHANY,
            user or MATCHANY,
        )
        matches = [
            con
            for con_id, con in self._connection_pool.items()
            if all(u == v for u, v in zip(match_tuple, con_id))
        ]

        if matches:
            return matches
        if default is not NOTSET:
            return default
        raise LookupError(f"{match_tuple} doesn't match any connections!")

    def _disconnect_id(self, conn_id: connection_id) -> None:
        self._connection_pool[conn_id].disconnect()
        del self._connection_pool[conn_id]

    def disconnect(
        self, *servers: str, conn_id: Optional[connection_id] = None
    ) -> None:
        """Disconnect the client completely, from certain servers, or from a specific id

        disconnect() -> disconnects client from everything.
        disconnect(*servers) -> disconnects every connection connected to one of servers
        disconnect(conn_id=id) -> disconnects specific id, raises error if id not found.
        """
        if conn_id is not None:
            discon_ids = (conn_id,)
        elif not servers:
            discon_ids = self._connection_pool.copy().keys()
        else:
            discon_ids = [
                con_id
                for con_id in self._connection_pool
                if con_id.destination in servers
            ]
        if servers and not discon_ids:
            raise LookupError(f"No connections have servers ({', '.join(servers)})")
        for con_id in discon_ids:
            self._disconnect_id(con_id)

    def connect(
        self,
        dest: str,
        *addtnl_dests: str,
        auth: Optional[Tuple[str, str]] = None,
        cfg: Optional[ConnectionConfig] = None,
        **cfg_kwargs: Any,
    ) -> "AmqpClient":
        usr, pwd = auth if auth is not None else (None, None)
        cfg = cfg if cfg is not None else ConnectionConfig(**cfg_kwargs)
        to_connect = (dest,) + addtnl_dests

        # Make sure all ids are new
        new_ids = []
        for server in to_connect:
            if to_connect.count(server) > 1:
                raise ValueError("All servers in 'connect' call must be different!")
            new_con = self._con_cls(server, usr=usr, pwd=pwd, cfg=cfg)
            conn_id = connection_id(
                server, cfg.RABBITMQ_PORT, cfg.VIRTUAL_HOST, new_con.user
            )
            if conn_id in self._connection_pool:
                raise ValueError(f"Client already connected to {new_con}")
            new_ids.append((conn_id, new_con))

        try:
            for conn_id, new_con in new_ids:
                self._connection_pool[conn_id] = new_con
                self._connection_pool[conn_id].connect()
        except ConnectionError as e:
            # Either everything connects or nothing does
            for conn_id, _ in new_ids:
                if conn_id in self._connection_pool:
                    self._disconnect_id(conn_id)
            raise ConnectionError(f"Couldn't connect to {', '.join(to_connect)}") from e
        return self

    def publish(
        self,
        msg: Any,
        route_key: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> None:
        for _, connection in self._connection_pool.items():
            if connection.state is not ConnectionState.CONNECTED:
                if (
                    connection.state is ConnectionState.CONNECTING
                    and connection.config.DROP_WHILE_RECONNECT
                ):
                    LOGGER.debug(
                        f"Dropping message to {connection}:{exchange}-{route_key} "
                        "reconnecting..."
                    )
                    continue
                pub_block = False
            else:
                pub_block = True
            connection.actor.publish(
                msg, route_key=route_key, exchange=exchange, block=pub_block
            )

    def __str__(self) -> str:
        return f"[Amqp Client] connected to: {', '.join(self.servers)}"

    def __repr__(self) -> str:
        return (
            "<AMQPClient>["
            f"{','.join([str(con) for _, con in self._connection_pool.items()])}"
            "]"
        )

    def __iter__(self):
        return iter(self._connection_pool.values())

    def __enter__(self) -> "AmqpClient":
        return self

    def __exit__(self, *args) -> None:
        self.disconnect()
