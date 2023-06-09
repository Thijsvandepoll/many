import os

import pytest

from many import Revisions
from many.migrate import Migrator
from tests.utils import LocalMigrationEngine, read_file


def test_migrate_up_down(tmp_path, fake_local_migrations):
    os.chdir(tmp_path)

    engine = LocalMigrationEngine()
    revisions = Revisions(fake_local_migrations)
    migrator = Migrator(engine=engine, revisions=revisions)

    # Test if migration can happen when not initialized
    with pytest.raises(ValueError):
        migrator.up()

    migrator.init()
    assert os.path.exists("state.txt")

    # Migrate up one
    migrator.up(level="1")
    assert os.path.exists("data_store.txt")

    file = read_file("data_store.txt")
    assert file == "Hello world!"
    assert migrator.get_current_state() == "v1"

    migrator.up()
    assert read_file("data_store.txt") == "Bye world!"
    assert migrator.get_current_state() == "v2"

    # Migrate one down
    migrator.down(level="1")
    assert read_file("data_store.txt") == "Hello world!"
    assert migrator.get_current_state() == "v1"

    # Migrate one up
    migrator.up(level="1")
    assert read_file("data_store.txt") == "Bye world!"
    assert migrator.get_current_state() == "v2"

    # Migrate down to base
    migrator.down()
    assert not os.path.exists("data_store.txt")
    assert migrator.get_current_state() is None
