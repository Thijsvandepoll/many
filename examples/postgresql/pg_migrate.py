from contextlib import contextmanager
from typing import Any, Dict, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from many import MigrationEngine, init_app
from many.templates import sqlalchemy_template

engine = create_engine(f"postgresql+psycopg2://root:root@localhost:5432/mydatabase")
session_factory = sessionmaker(bind=engine, autoflush=True)
Session = scoped_session(session_factory)


@contextmanager
def pg_session():
    session = Session()
    try:
        yield session
    except SystemExit as ext:
        if ext.code == 0:
            session.commit()
        else:
            session.rollback()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


class PostgresEngine(MigrationEngine):
    def __init__(self, schema="migrations", table: str = "migrations"):
        self.schema = schema
        self.table = table

    def init_remote(self):
        Session().execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema}"))
        Session().execute(
            text(
                f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.table} (version"
                " VARCHAR(10))"
            )
        )
        Session().execute(
            text(f"INSERT INTO {self.schema}.{self.table} (version) VALUES (NULL)")
        )

    def remote_exists(self) -> bool:
        return bool(
            Session()
            .execute(
                text(
                    "SELECT schema_name FROM information_schema.schemata WHERE"
                    f" schema_name = '{self.schema}'"
                )
            )
            .first()
        )

    def update_remote(self, state: str):
        if state is None:
            state = "NULL"
        else:
            state = f"'{state}'"
        Session().execute(
            text(f"UPDATE {self.schema}.{self.table} SET version = {state}")
        )

    def get_remote(self) -> str:
        version = (
            Session()
            .execute(text(f"SELECT version FROM {self.schema}.{self.table}"))
            .first()
        )
        if version:
            return version[0]

    def prepare_args(self, **app_kwargs) -> Tuple[Tuple[Any], Dict[Any, Any]]:
        return (Session(),), app_kwargs


if __name__ == "__main__":
    with pg_session():
        app = init_app(
            migration_engine=PostgresEngine(),
            template=sqlalchemy_template,
        )
        app()
