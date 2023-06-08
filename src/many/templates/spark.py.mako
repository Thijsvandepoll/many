from pyspark.sql import SparkSession

version = ${repr(version)}
down_version = ${repr(down_version)}


def up(session: SparkSession):
    # Insert your UP migration below
    ...


def down(session: SparkSession):
    # Insert your DOWN migration below
    ...