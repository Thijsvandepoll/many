import os
from configparser import ConfigParser
from typing import Annotated, Optional

import typer
from typer import Option

from many.engine import MigrationEngine
from many.migrate import Migrator
from many.revise import Revisions
from many.templates import Template, base_template
from many.utils import resolve_kwargs


def common_options_callback(ctx: typer.Context, value: Optional[str]):
    """Callback function to collect options in the context."""
    if ctx.resilient_parsing:
        return
    if value is not None:
        # Ensure we have a dict to store options in the context
        if not ctx.obj:
            ctx.obj = {}
        # Store the option and its value
        ctx.obj[ctx.current_parameter.name] = value


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

    @app.command(
        help="Command to upgrade the data store",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    )
    def up(ctx: typer.Context, level: str = "head"):
        migrator.up(level=level, **resolve_kwargs(ctx.args))

    @app.command(
        help="Command to downgrade the data store",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    )
    def down(ctx: typer.Context, level: str = 1):
        migrator.down(level=level, **resolve_kwargs(ctx.args))

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
