# Migrating Iceberg
This is a small example to showcase implementing a Iceberg migration application. This is originally why I needed some customizable migration tool.

## Getting started
- Make sure `pyspark==3.3` is installed using: `pip install pyspark==3.3`
- Make sure `many` is installed, for example run `pip install .` from the project's root.
- Make sure a local Minio is running as S3 object storage by running `docker-compose up --build`

## Creating the application:
I created a simple sample application by subclassing the `MigrationEngine` class and implementing the required methods to update the remote state tracking using Apache Iceberg. I have implemented this using PySpark, but probably there are other ways to do this using PyIceberg. There is a lot of configurations required for the SparkSession to make spark communicate to the Minio cluster and manage the Iceberg tables. An example is used here, but it can be modified to also use a Hive Metastore.

## Running the application
Create a first migration by running:
```
python ib_migrate.py revision create -m "My first migration"
```

Modify the created template to customize the first migration to your needs, say:
```
def up(session: SparkSession):
    session.sql("CREATE NAMESPACE IF NOT EXISTS twitter;")
    session.sql(
        "CREATE TABLE twitter.tweets (user STRING, post_date DATE, message STRING);"
    )


def down(session: SparkSession):
    session.sql("DROP TABLE twitter.tweets;")
```

Initialize the remote state by running:
```
python ib_migrate.py migrate init
```

Upgrade Iceberg by running:
```
python ib_migrate.py migrate up
```

Using a small python script reusing the `get_session()` function, it is possible to verify that the remote state has been updated and that the table exists:
```
# This shows that the state has been updated
get_session().sql("SELECT * FROM migrations.migrations").show()

# This shows that the table exists
get_session().sql("SELECT * FROM twitter.tweets").show()
```

Now we can create a second migration which will insert some data:
```
python ib_migrate.py revision create -m "Insert some data"
```

Modify the template to insert some data:
```
def up(session: SparkSession):
    df = session.createDataFrame(
        [
            ("kimchi", datetime.date(2010, 1, 1), "Some first tweet."),
            ("elon", datetime.date(2010, 1, 2), "Some second tweet."),
        ],
        schema=tp.StructType(
            [
                tp.StructField("user", tp.StringType()),
                tp.StructField("post_date", tp.DateType()),
                tp.StructField("message", tp.StringType()),
            ]
        ),
    )
    df.write.format("iceberg").mode("append").save("twitter.tweets")


def down(session: SparkSession):
    session.sql("DELETE FROM twitter.tweets;")
```

Now running another upgrade will insert the data into Iceberg:
```
python ib_migrate.py migrate up
```

One can now verify that the data has been inserted. Now we can run a downgrade to undo all migrations:
```
python ib_migrate.py migrate down --level base
```

## Clean up
To clean up the resources, run:
```
docker-compose down
```