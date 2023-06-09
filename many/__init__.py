import os
from configparser import ConfigParser
from typing import Annotated

import typer
from typer import Option

from many.engine import MigrationEngine
from many.migrate import Migrator
from many.revise import Revisions
from many.templates import Template, base_template


def _init_revision_app(revisions: Revisions):
    app = typer.Typer()

    @app.command(help="Create new revision")
    def create(m: Annotated[str, Option("-m")]):
        revisions.create_revision(m=m)

    return app


def _init_migration_app(engine: MigrationEngine, revisions: Revisions):
    app = typer.Typer()

    migrator = Migrator(engine=engine, revisions=revisions)

    @app.command(help="Command to initialize the migrations")
    def init():
        migrator.init()

    @app.command(help="Command to upgrade the data store")
    def up(level: str = "head"):
        migrator.up(level=level)

    @app.command(help="Command to downgrade the data store")
    def down(level: str = 1):
        migrator.down(level=level)

    return app


def init_app(
    migration_engine: MigrationEngine,
    template: Template = base_template,
    config_file: str = None,
):
    conf = ConfigParser()
    conf.read(config_file or os.path.dirname(__file__) + "/default-config.ini")

    app = typer.Typer()
    revisions = Revisions(
        script_location=conf["revisions"]["script_location"],
        file_template=conf["revisions"]["file_template"],
        truncate_slug_length=int(conf["revisions"]["truncate_slug_length"]),
        template=template,
    )
    revision_app = _init_revision_app(revisions=revisions)
    migrator_app = _init_migration_app(engine=migration_engine, revisions=revisions)

    app.add_typer(revision_app, name="revision")
    app.add_typer(migrator_app, name="migrate")

    return app
