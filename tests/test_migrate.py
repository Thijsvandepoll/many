import os

import pytest

from many.migrate import Migrator
from many.revise import Revisions
from tests.utils import LocalMigrationEngine, read_file


def test_migrate_up_down(tmp_path, fake_local_migrations):
    os.chdir(tmp_path)

    engine = LocalMigrationEngine()
    revisions = Revisions(fake_local_migrations)
    app = Migrator(engine=engine, revisions=revisions)

    # Test if migration can happen when not initialized
    with pytest.raises(ValueError):
        app.up()

    app.init()
    assert os.path.exists("state.txt")

    # Migrate up one
    app.up(level="1")
    assert os.path.exists("data_store.txt")

    file = read_file("data_store.txt")
    assert file == "Hello world!"
    assert app.get_current_state() == "v1"

    with pytest.raises(SystemExit):
        # Migrate up head
        app.up()
    assert read_file("data_store.txt") == "Bye world!"
    assert app.get_current_state() == "v2"

    # Migrate one down
    app.down(level="1")
    assert read_file("data_store.txt") == "Hello world!"
    assert app.get_current_state() == "v1"

    # Migrate one up
    app.up(level="1")
    assert read_file("data_store.txt") == "Bye world!"
    assert app.get_current_state() == "v2"

    # Migrate down to base
    with pytest.raises(SystemExit):
        app.down()
    assert not os.path.exists("data_store.txt")
    assert app.get_current_state() is None
