from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


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

    def prepare_args(self, **app_kwargs) -> Tuple[Tuple[Any], Dict[Any, Any]]:
        return ((),), app_kwargs
