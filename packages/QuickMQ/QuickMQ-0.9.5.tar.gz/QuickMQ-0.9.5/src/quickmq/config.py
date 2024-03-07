"""
quickmq.config
~~~~~~~~~~~~~~

Classes, methods, and variables useful to the configuration of quickmq.
"""

import contextlib
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

CfgValue = TypeVar("CfgValue", str, int, float)


class ConfigDefault(Enum):
    DEFAULT_USER = "guest"
    DEFAULT_PASS = "guest"
    RABBITMQ_PORT = 5672
    VIRTUAL_HOST = "/"
    DEFAULT_EXCHANGE = ""
    DEFAULT_ROUTE_KEY = ""
    RECONNECT_TRIES = 5
    RECONNECT_DELAY = 10.0
    DROP_WHILE_RECONNECT = True


def positive_validator(name: str, value: Any) -> None:
    if value <= 0:
        raise ValueError(f"Values for {name!r} must be positive!")


def non_negative_validator(name: str, value: Any) -> None:
    if value < 0:
        raise ValueError(f"Values for {name!r} must be larger than 0!")


class ConfigVariable(Generic[CfgValue]):
    def __init__(
        self,
        type: Type[CfgValue],
        default: Union[CfgValue, ConfigDefault],
        validators: Iterable[Callable[[str, CfgValue], None]] = (),
    ) -> None:
        self.type: Type[CfgValue] = type
        self.validators: Iterable[Callable[[str, CfgValue], None]] = validators
        if isinstance(default, ConfigDefault):
            self.default = default.value
        else:
            self.default = default

    def __set_name__(self, owner: Type[object], name: str) -> None:
        self.name = name

    @overload
    def __get__(self, instance: None, owner: Type[object]) -> "ConfigVariable":
        """Called when an attribute is accessed via class not an instance"""

    @overload
    def __get__(self, instance: object, owner: Type[object]) -> CfgValue:
        """Called when an attribute is accessed via an instance"""

    def __get__(
        self, instance: Union[object, None], owner: Type[object]
    ) -> Union["ConfigVariable", CfgValue]:
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: object, nValue: Optional[Any]) -> None:
        if nValue is None or isinstance(nValue, ConfigVariable):
            instance.__dict__[self.name] = self.default
            return
        with contextlib.suppress(ValueError):
            nValue = self.type(nValue)  # duck typing
        if not isinstance(nValue, self.type):
            raise TypeError(f"{self.name!r}  values must be of type {self.type!r}")
        for validate in self.validators:
            validate(self.name, nValue)
        instance.__dict__[self.name] = nValue

    def __delete__(self, obj) -> None:
        raise AttributeError("Cannot delete config attributes!")

    def __str__(self) -> str:
        return f"Config variable: {self.name}"

    def __repr__(self) -> str:
        return f"ConfigVariable<{self.name}>(type={self.type},def={self.default})"


@dataclass
class ConnectionConfig:
    RECONNECT_DELAY: float = ConfigVariable(
        float,
        ConfigDefault.RECONNECT_DELAY,
        [
            non_negative_validator,
        ],
    )  # type: ignore [assignment]
    RECONNECT_TRIES: int = ConfigVariable(int, ConfigDefault.RECONNECT_TRIES)  # type: ignore [assignment]
    DEFAULT_EXCHANGE: str = ConfigVariable(str, ConfigDefault.DEFAULT_EXCHANGE)  # type: ignore [assignment]
    RABBITMQ_PORT: int = ConfigVariable(
        int,
        ConfigDefault.RABBITMQ_PORT,
        [
            positive_validator,
        ],
    )  # type: ignore [assignment]
    VIRTUAL_HOST: str = ConfigVariable(str, ConfigDefault.VIRTUAL_HOST)  # type: ignore [assignment]
    DEFAULT_USER: str = ConfigVariable(str, ConfigDefault.DEFAULT_USER)  # type: ignore [assignment]
    DEFAULT_PASS: str = ConfigVariable(str, ConfigDefault.DEFAULT_PASS)  # type: ignore [assignment]
    DEFAULT_ROUTE_KEY: str = ConfigVariable(str, ConfigDefault.DEFAULT_ROUTE_KEY)  # type: ignore [assignment]
    DROP_WHILE_RECONNECT: bool = ConfigVariable(
        bool, ConfigDefault.DROP_WHILE_RECONNECT
    )  # type: ignore [assignment]
