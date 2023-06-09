# Many: A library to migrate anything!
Managing state changes in data stores is an important part of the development process. There are many great migration tool available for SQL-like databases. However, there is lack of support for other data stores. Because of that I created a small library called `many` which can be used to build your own migration tool for any data store.

## Creating your own application
To create your own migration application for your data store:
1. Subclass the `MigrationEngine` class and implement its methods.
2. Optionally, create a customized migration template by using `Mako` templates.
3. Initialize your application using `init_app` function with your customized `MigrationEngine` and `Template`
4. Run you application.

How this would look like:
```python
# migration_app.py

from many import MigrationEngine, init_app

class CustomEngine(MigrationEngine):
    def init_remote(self):
        # Add logic to initialize a place where the state can be maintained (e.g. a table).

    def remote_exists(self) -> bool:
        # Add logic to check whether the remote state exists.

    def update_remote(self, state: str):
        # Add logic to update the remote state to the provided state

    def get_remote(self) -> str:
        # Add logic to get the remote state 

    def prepare_args(self) -> Tuple[Any]:
        # Logic to pass any argument to the actual migration (e.g. a session/connection object).
        
if __name__ == "__main__":
    app = init_app(CustomEngine())
    app()
```

Now, this application can be used as follows:
1. `python migration_app.py revision create -m "My first migration"` to create your first revision in the `versions` folder.
2. Modify the generated file in the `versions` to customize your migration.
3. `python migration_app.py migrate up` to upgrade the state to the latest migration.
4. `python migration_app.py migrate down` to downgrade the state one level. Use `python migration_app.py migrate down --level base` to downgrade completely.

## Examples
I have added some examples to showcase how to use the library by implementing some migration applications for:
- Elasticsearch: `examples/elasticsearch`
- Apache Iceberg: `examples/iceberg`
- PostgreSQL: `examples/postgresql`



