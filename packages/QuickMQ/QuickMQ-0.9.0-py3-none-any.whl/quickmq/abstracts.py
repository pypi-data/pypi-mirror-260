import logging
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from functools import partialmethod
from queue import Queue
from threading import Event, Lock, Thread
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from .config import ConnectionConfig
from .exceptions import WrongStateError
from .utils import encode_message

LOGGER = logging.getLogger("quickmq")
_IMPL_ERROR_STR = "Implement in child class"

# Types for Generic Class
ACTOR = TypeVar("ACTOR", bound="BaseActor")
CONN = TypeVar("CONN", bound="BaseConnection")

# Types for sched_action
V = TypeVar("V")


class ConnectionState(Enum):
    INITIALIZED = 0
    CONNECTING = 10
    CONNECTED = 20
    DISCONNECTING = 30
    DISCONNECTED = 40

    def is_state(self, state: int) -> bool:
        return self.value == state

    is_connecting = partialmethod(is_state, 10)
    is_connected = partialmethod(is_state, 20)
    is_disconnecting = partialmethod(is_state, 30)
    is_disconnected = partialmethod(is_state, 40)


class StateTracker:
    def __init__(self, init_state: ConnectionState) -> None:
        self._edit_lock = Lock()
        self._state_events: Dict[ConnectionState, Event] = {}
        for state in ConnectionState:
            self._state_events[state] = Event()
        self.__internal_state = init_state
        self._state_events[self.__internal_state].set()

    @property
    def state(self) -> ConnectionState:
        with self._edit_lock:
            return self.__internal_state

    @state.setter
    def state(self, new_state: ConnectionState) -> None:
        with self._edit_lock:
            self._state_events[self.__internal_state].clear()
            self.__internal_state = new_state
            self._state_events[new_state].set()

    def wait(self, state: ConnectionState, timeout: Optional[float] = None) -> None:
        self._state_events[state].wait(timeout=timeout)


# class Editor(ABC):
#     """
#     Responsabilities: Edit the topology of the RabbitMQ connection,
#     e.g. creating/editing/deleting queues/exchanges.
#     """
#     def __init__(self, con: Connection) -> None:
#         self._con = con

#     @property
#     def connection(self) -> Connection:
#         return self._con


class BaseActor(Generic[CONN], ABC):
    """
    Responsabilities: perform actions on a connection e.g. publish/consume/get/etc.

    Possible future responsabilites: nack, recover, reject, qos.
    """

    def __init__(self, con: "CONN") -> None:
        self._con = con

    def publish(
        self,
        msg: Any,
        route_key: Optional[str] = None,
        exchange: Optional[str] = None,
        block=True,
    ) -> None:
        route_key = route_key or self._con.config.DEFAULT_ROUTE_KEY
        exchange = exchange or self._con.config.DEFAULT_EXCHANGE
        msg_bytes = encode_message(msg)
        self._con.sched_action(
            self._publish,
            block=block,
            con=self._con,
            msg=msg_bytes,
            route_key=route_key,
            exchange=exchange,
        )

    @abstractmethod
    def _publish(self, con: "CONN", msg: bytes, route_key: str, exchange: str) -> None:
        raise NotImplementedError(_IMPL_ERROR_STR)

    # vvv To be implemented vvv
    # def consume(cls, con: Connection) -> Callable:
    #     pass

    # def get(cls, block=False) -> Callable:
    #     pass


class BaseConnection(Generic[ACTOR], ABC):
    "Abstract class for a connection that handles the state and thread management"

    def __init__(
        self,
        destination: str,
        usr: Optional[str] = None,
        pwd: Optional[str] = None,
        cfg: Optional[ConnectionConfig] = None,
    ) -> None:
        # Properties that should be accessed through @property
        self._config = cfg or ConnectionConfig()
        self._dest = destination

        # Properties that could be useful for the implemented class
        self._action_queue: Queue[Tuple[Callable, Dict[str, Any]]] = Queue()
        self._action_err: Optional[Exception] = None
        self._action_rv: Any = None

        self._usr = usr or self._config.DEFAULT_USER
        self._pwd = pwd or self._config.DEFAULT_PASS

        # Properties to keep to the abstract base class
        self.__st_track = StateTracker(ConnectionState.INITIALIZED)
        self.__con_thread = Thread(target=self._run, name=f"{str(self)}", daemon=True)

    @property
    @abstractmethod
    def actor(self) -> ACTOR:
        raise NotImplementedError(_IMPL_ERROR_STR)

    @property
    def state(self) -> ConnectionState:
        return self.__st_track.state

    @property
    def destination(self) -> str:
        return self._dest

    @property
    def user(self) -> str:
        return self._usr

    @property
    def config(self) -> ConnectionConfig:
        return self._config

    def connect(self) -> "BaseConnection":
        # Thread management
        if not self.__con_thread.is_alive():
            LOGGER.debug(f"Starting connection thread to {self._dest}")
            self.__con_thread.start()  # Thread needs to start before CONNECTING

        # State management
        LOGGER.debug(f"Connecting to {self._dest}")
        try:
            self.__st_track.state = ConnectionState.CONNECTING
            self._connect()
        except (ConnectionError, KeyboardInterrupt) as e:
            LOGGER.error(f"Error connecting to {self._dest!r}, {e}")
            self.__st_track.state = ConnectionState.DISCONNECTED
            raise
        except WrongStateError:
            return self  #  Disconnected while reconnecting
        else:
            self.__st_track.state = ConnectionState.CONNECTED
            LOGGER.info(f"Successfully connected to {self._dest}")

        return self

    def disconnect(self):
        if self.__st_track.state not in (
            ConnectionState.CONNECTED,
            ConnectionState.CONNECTING,
        ):
            return
        LOGGER.debug(f"Disconnecting from {self._dest}")
        self.__st_track.state = ConnectionState.DISCONNECTING
        try:
            self._disconnect()
        except (Exception, KeyboardInterrupt) as e:
            LOGGER.error(f"Error while disconnecting from {self._dest!r}, {e}")
            warnings.warn(
                f"Error while disconnecting from {self._dest!r}, {e}",
                category=RuntimeWarning,
                stacklevel=2,
            )
        finally:
            self.__st_track.state = ConnectionState.DISCONNECTED
            LOGGER.info(f"Disconnected from {self._dest}")

    @overload
    def sched_action(
        self, action: Callable[..., V], block: Literal[False] = False, **act_kwargs: Any
    ) -> None:
        ...

    @overload
    def sched_action(
        self, action: Callable[..., V], block: Literal[True] = True, **act_kwargs: Any
    ) -> V:
        ...

    def sched_action(
        self, action: Callable[..., V], block: bool = True, **act_kwargs: Any
    ) -> Union[None, V]:
        if self.__st_track.state not in (
            ConnectionState.CONNECTED,
            ConnectionState.CONNECTING,
        ):
            raise WrongStateError(
                f"Cannot schedule action {action.__name__!r} "
                "while not connected or connecting!"
            )
        LOGGER.debug(f"Scheduling action {action!r}, blocking? {block}")
        self._action_queue.put((action, act_kwargs))
        if not block:
            return None
        self._action_queue.join()
        if self._action_err is None:
            rv = self._action_rv
            self._action_rv = None
            return rv
        e = self._action_err
        self._action_err = None
        raise e

    def wait_for_state(
        self, state: ConnectionState, timeout: Optional[float] = None
    ) -> None:
        self.__st_track.wait(state, timeout)

    def join(self, timeout: Optional[float] = None) -> None:
        if self.state is ConnectionState.INITIALIZED:
            raise WrongStateError("Cannot join connection before connecting!")
        self.__con_thread.join(timeout=timeout)
        if timeout is not None and self.__con_thread.is_alive():
            raise TimeoutError(f"Connection thread didn't join after {timeout} seconds")

    @abstractmethod
    def _run(self) -> None:
        self.wait_for_state(ConnectionState.CONNECTING)
        while self.state.is_connecting():
            self.wait_for_state(ConnectionState.CONNECTED, timeout=0.5)
        if self.state in (ConnectionState.DISCONNECTED, ConnectionState.DISCONNECTING):
            return

    @abstractmethod
    def _connect(self) -> None:
        raise NotImplementedError(_IMPL_ERROR_STR)

    @abstractmethod
    def _disconnect(self) -> None:
        raise NotImplementedError(_IMPL_ERROR_STR)

    def __enter__(self) -> "BaseConnection":
        if self.__st_track.state is ConnectionState.INITIALIZED:
            self.connect()
        return self

    def __exit__(self, *args) -> None:
        self._action_queue.join()
        self.disconnect()
        self.join()

    def __str__(self) -> str:
        return (
            f"AmqpConnection({self._dest}:{self._config.RABBITMQ_PORT})"
            f"<vhost:{self._config.VIRTUAL_HOST!r}><user:{self._usr}>"
        )
