from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


class Request(ABC):  # pylint: disable=too-few-public-methods
    @property
    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...


R = TypeVar("R", bound=Request)


class Adapter(ABC, Generic[R]):
    @abstractmethod
    def get_response(self, request: R) -> str: ...
