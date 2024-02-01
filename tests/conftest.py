import os

import pytest

from tests.utils import write_file

revision1 = """
import os

version = "v1"
down_version = None


def up(*args, **kwargs):
    with open("data_store.txt", "w") as f:
        f.write("Hello world!")

def down(*args, **kwargs):
    os.remove("data_store.txt")
"""

revision2 = """
version = "v2"
down_version = "v1"

def up(*args, **kwargs):
    with open("data_store.txt", "w") as f:
        f.write("Bye world!")

def down(*args, **kwargs):
    with open("data_store.txt", "w") as f:
        f.write("Hello world!")
"""

revision_with_kwargs = """
version = "v1"
down_version = None

def up(*args, **kwargs):
    with open("data_store.txt", "w") as f:
        f.write(kwargs['some_kwarg_up'])

def down(*args, **kwargs):
    with open("data_store.txt", "w") as f:
        f.write(kwargs['some_kwarg_down'])
"""


@pytest.fixture
def fake_local_migrations(tmp_path):
    tmp_path = str(tmp_path)
    script_location = "versions"
    os.mkdir(tmp_path + "/" + script_location)
    write_file(tmp_path + f"/{script_location}/revision1.py", revision1)
    write_file(tmp_path + f"/{script_location}/revision2.py", revision2)
    return script_location


@pytest.fixture
def fake_local_migration_with_args_kwargs(tmp_path):
    tmp_path = str(tmp_path)
    script_location = "versions"
    os.mkdir(tmp_path + "/" + script_location)
    write_file(tmp_path + f"/{script_location}/revision1.py", revision_with_kwargs)
    return script_location
