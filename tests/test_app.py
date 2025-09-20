import os

from typer.testing import CliRunner

from many import init_app
from tests.utils import LocalMigrationEngine, read_file


def test_app(tmp_path, fake_local_migrations):
    os.chdir(tmp_path)

    app = init_app(migration_engine=LocalMigrationEngine(str(tmp_path)))
    runner = CliRunner()

    # Init
    result = runner.invoke(app, ["migrate", "init"])
    assert result.exit_code == 0

    # Upgrade
    result = runner.invoke(app, ["migrate", "up"])
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Bye world!"

    # Another init should just skip]
    result = runner.invoke(app, ["migrate", "up"])
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Bye world!"

    # Down revision is a single one
    result = runner.invoke(app, ["migrate", "down"])
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Hello world!"

    # Test random init (no change)
    result = runner.invoke(app, ["migrate", "init"])
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Hello world!"

    # Create a new revision
    result = runner.invoke(app, ["revision", "create", "Another migration"])
    assert result.exit_code == 0
    assert len(os.listdir("versions")) == 3


def test_app_with_kwargs(tmp_path, fake_local_migration_with_args_kwargs):
    os.chdir(tmp_path)

    app = init_app(migration_engine=LocalMigrationEngine(str(tmp_path)))
    runner = CliRunner()

    # Init
    result = runner.invoke(app, ["migrate", "init"])
    assert result.exit_code == 0

    # Upgrade
    result = runner.invoke(app, ["migrate", "up", "--some_kwarg_up", "Some value"])
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Some value"

    # Downgrade
    result = runner.invoke(
        app, ["migrate", "down", "--some_kwarg_down", "Some other value"]
    )
    assert result.exit_code == 0
    assert read_file("data_store.txt") == "Some other value"
