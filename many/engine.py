from abc import ABC, abstractmethod
from typing import Any, Tuple


class MigrationEngine(ABC):
    @abstractmethod
    def init_remote(self):
        ...

    @abstractmethod
    def remote_exists(self) -> bool:
        ...

    @abstractmethod
    def update_remote(self, state: str):
        ...

    @abstractmethod
    def get_remote(self) -> str:
        ...

    @abstractmethod
    def prepare_args(self) -> Tuple[Any]:
        ...
