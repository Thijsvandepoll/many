import os.path
from typing import Any, Tuple

from many.engine import MigrationEngine


def write_file(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)


def read_file(filename: str):
    with open(filename) as f:
        file = f.read()
    return file


class LocalMigrationEngine(MigrationEngine):
    def __init__(self, path: str = "."):
        self.path = path

    def init_remote(self):
        write_file(self.path + "/state.txt", content="")

    def remote_exists(self) -> bool:
        return os.path.isfile(self.path + "/state.txt")

    def update_remote(self, state: str):
        write_file(self.path + "/state.txt", repr(state))

    def get_remote(self) -> str:
        with open(self.path + "/state.txt", "r") as f:
            out = f.read()
        if out:
            return eval(out)

    def prepare_args(self) -> Tuple[Any]:
        return ((),)
