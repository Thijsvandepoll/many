import datetime
import inspect
import os
from unittest.mock import Mock

import pytest

import many
from many import Revisions
from tests.utils import read_file


class TestRevisions:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.tmp_path = str(tmp_path)

        # Change dir
        os.chdir(self.tmp_path)

    def test_collection(self, fake_local_migrations):
        collection = Revisions("versions")
        assert len(collection.revisions) == 2

        # Check if upgrades exist
        assert collection.has_upgrade(None)
        assert collection.has_upgrade("v1")
        assert not collection.has_upgrade("v2")

        # Check if downgrades exist
        assert collection.has_downgrade("v2")
        assert collection.has_downgrade("v1")
        assert not collection.has_downgrade(None)

        # Check source code of upgrades
        upgrade, new_state = collection.get_upgrade(None)
        assert (
            inspect.getsource(upgrade)
            == 'def up(*args, **kwargs):\n    with open("data_store.txt", "w") as f:\n '
            '       f.write("Hello world!")\n'
        )
        assert new_state == "v1"

        upgrade, new_state = collection.get_upgrade("v1")
        assert (
            inspect.getsource(upgrade)
            == 'def up(*args, **kwargs):\n    with open("data_store.txt", "w") as f:\n '
            '       f.write("Bye world!")\n'
        )
        assert new_state == "v2"

        downgrade, new_state = collection.get_downgrade("v2")
        assert (
            inspect.getsource(downgrade)
            == 'def down(*args, **kwargs):\n    with open("data_store.txt", "w") as'
            ' f:\n        f.write("Hello world!")\n'
        )
        assert new_state == "v1"

        downgrade, new_state = collection.get_downgrade("v1")
        assert (
            inspect.getsource(downgrade)
            == 'def down(*args, **kwargs):\n    os.remove("data_store.txt")\n'
        )
        assert new_state is None

    def test_create_revision(self, monkeypatch):
        now = Mock(return_value=datetime.datetime(2010, 1, 1, 0, 0, 0))
        monkeypatch.setattr(datetime, "datetime", Mock(now=now))
        monkeypatch.setattr(
            many.revise, "create_hash", lambda *args, **kwargs: "123abc"
        )

        revisions = Revisions("versions")

        # Check if no data is in the current directory
        assert os.listdir() == []

        # Create revision
        revisions.create_revision(m="My first migration")

        # Check if it created a directory using default configurations
        assert os.listdir() == ["versions"]
        assert os.listdir("versions") == [
            "2010_01_01_0000-123abc_my_first_migration.py"
        ]

        file = read_file("versions/2010_01_01_0000-123abc_my_first_migration.py")
        assert (
            file
            == "version = '123abc'\ndown_version = None\n\n\ndef up(*args):\n    #"
            " Insert your UP migration below\n    ...\n\n\ndef down(*args):\n    #"
            " Insert your DOWN migration below\n    ..."
        )

        monkeypatch.setattr(
            many.revise, "create_hash", lambda *args, **kwargs: "123xyz"
        )
        revisions.create_revision(m="My second migration")

        assert os.listdir("versions") == [
            "2010_01_01_0000-123abc_my_first_migration.py",
            "2010_01_01_0000-123xyz_my_second_migration.py",
        ]

        file = read_file("versions/2010_01_01_0000-123xyz_my_second_migration.py")
        assert (
            file
            == "version = '123xyz'\ndown_version = '123abc'\n\n\ndef up(*args):\n    #"
            " Insert your UP migration below\n    ...\n\n\ndef down(*args):\n    #"
            " Insert your DOWN migration below\n    ..."
        )
