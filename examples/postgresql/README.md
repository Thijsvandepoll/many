# Migrating Postgres
Although there is many migration tools for SQL databases, I implemented a small example using SQLAlchemy for Postgres to showcase the flexibility.

## Getting started
- Make sure `sqlalchemy` and `psycopg2-binary` by running: `pip install sqlalchemy psycopg2-binary`
- Make sure `many` is installed, for example run `pip install .` from the project's root.
- Make sure local Postgres is running using: `docker-compose up --build`

## Creating the application
I have created a small example application by subclassing `MigrationEngine` class.

## Running the application
To create the revision:
```
python pg_migrate.py revision create -m "My first migration"
```

To upgrade:
```
python pg_migrate.py migrate up
```

To downgrade:
```
python pg_migrate.py migrate down --level base
```

## Clean up
Run `docker-compose down`
