import os

import pytest

from tests.utils import write_file

revision1 = """
import os

version = "v1"
down_version = None


def up(*args):
    with open("data_store.txt", "w") as f:
        f.write("Hello world!")

def down(*args):
    os.remove("data_store.txt")
"""

revision2 = """
version = "v2"
down_version = "v1"

def up(*args):
    with open("data_store.txt", "w") as f:
        f.write("Bye world!")

def down(*args):
    with open("data_store.txt", "w") as f:
        f.write("Hello world!")
"""


@pytest.fixture
def fake_local_migrations(tmp_path):
    tmp_path = str(tmp_path)
    script_location = "versions"
    os.mkdir(tmp_path + "/" + script_location)
    write_file(tmp_path + f"/{script_location}/revision1.py", revision1)
    write_file(tmp_path + f"/{script_location}/revision2.py", revision2)
    return script_location
