# Migrating Elasticsearch
This is a small example to showcase implementing a Elasticsearch migration application.

## Getting started
- Make sure `elasticsearch` and `elasticsearch-dsl` are installed using: `pip install elasticsearch elasticsearch-dsl`
- Make sure `many` is installed, for example run `pip install .` from the project's root.
- Make sure a local Elasticsearch and Kibana cluster are running by running `docker-compose up --build`

## Creating the application
I created a simple sample application by subclassing the `MigrationEngine` class and implementing the required methods for it using the Elasticsearch python client. A small summary of the methods:
- `init_remote()`: initializes the remote state tracking index on the Elasticsearch cluster
- `remote_exists()`: checks whether the remote state tracking index exists
- `update_remote()`: updates the remote state tracking to the provided state
- `get_remote()`: gets the value from the remote state tracking
- `prepare_args()`: method to pass arguments to the `up` and `down` functions in the revision templates

## Running the application
Create a first migration by running:
```
python es_migrate.py revision create -m "My first migration"
```

Modify the created template to customize the first migration to your needs, say:
```python
def up(connection: Elasticsearch):
    connection.indices.create(
        index="twitter",
        body={
            "mappings": {
                "properties": {
                    "user": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                    },
                    "post_date": {"type": "date"},
                    "message": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                    },
                }
            }
        },
    )


def down(connection: Elasticsearch):
    connection.indices.delete(index="twitter")
```

Now, initialize the remote state by running:
```
python es_migrate.py migrate init
```

Upgrade Elasticsearch by running migrations:
```
python es_migrate.py migrate up
```

From Kibana or using `curl` you can verify that the migration state has been updated on Elasticsearch, and the `twitter` index has been created with the right mapping. Now we can create another migration to insert some data:
```
python es_migrate.py revision create -m "Insert some data"
```

Modify the created template to insert some data, say:
```python
def up(connection: Elasticsearch):
    connection.index(
        index="twitter",
        body={
            "user": "kimchi",
            "post_date": datetime.date(2010, 1, 1),
            "message": "This is a first message",
        },
        id="1",
    )
    connection.index(
        index="twitter",
        body={
            "user": "elon",
            "post_date": datetime.date(2010, 1, 2),
            "message": "This a second one.",
        },
        id="2",
    )


def down(connection: Elasticsearch):
    connection.delete(index="twitter", id="1")
    connection.delete(index="twitter", id="2")
```

Now, upgrade Elasticsearch again by running an upgrade:
```
python es_migrate.py migrate up
```

Verify that the record have been inserted. Now we can run a downgrade to undo all migrations:
```
python es_migrate.py migrate down --level base
```

## Clean up
To clean up the example, run:
```
docker-compose down
```

