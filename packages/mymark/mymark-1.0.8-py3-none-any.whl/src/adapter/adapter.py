from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class Request(ABC):  # pylint: disable=too-few-public-methods
    @property
    @abstractmethod
    def query(self) -> str: ...


R = TypeVar("R", bound=Request)


class Adapter(ABC, Generic[R]):
    @abstractmethod
    def get_response(self, request: R) -> str: ...

    @abstractmethod
    def get_responses(self, requests: list[R]) -> list[str]: ...
