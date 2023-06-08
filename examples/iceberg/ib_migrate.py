import os
from typing import Any, Tuple

from pyspark.sql import SparkSession

from many import MigrationEngine, init_app
from many.templates import spark_template

spark: SparkSession = None


def get_session() -> SparkSession:
    global spark
    if not spark:
        # Ensure dependencies are added
        dependencies = [
            "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.2.1",
            "org.apache.iceberg:iceberg-aws:1.2.1",
            "org.apache.hadoop:hadoop-aws:3.2.2",
            "com.amazonaws:aws-java-sdk:1.11.563",
            "software.amazon.awssdk:bundle:2.17.257",
            "software.amazon.awssdk:url-connection-client:2.17.257",
        ]
        os.environ[
            "PYSPARK_SUBMIT_ARGS"
        ] = f"--packages {','.join(dependencies)} pyspark-shell"
        os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"

        # Create builder
        builder = SparkSession.builder.appName("IcebergMigrations")

        # Add iceberg configurations
        builder = (
            builder.config(
                "spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            )
            .config(
                "spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog"
            )
            .config("spark.sql.catalog.my_catalog.type", "hadoop")
            .config(
                "spark.sql.catalog.my_catalog.warehouse", "s3a://lakehouse/my_catalog"
            )
            .config(
                "spark.sql.catalog.my_catalog.io-impl",
                "org.apache.iceberg.aws.s3.S3FileIO",
            )
            .config("spark.sql.defaultCatalog", "my_catalog")
            .config("spark.sql.catalog.my_catalog.s3.endpoint", "http://localhost:9000")
        )

        # Add hadoop configurations
        builder = (
            builder.config("spark.hadoop.fs.s3a.access.key", "minioadmin")
            .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
            .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
            .config(
                "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
            )
            .config(
                "spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            )
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
        )

        spark = builder.getOrCreate()
    return spark


class IcebergEngine(MigrationEngine):
    def __init__(self, namespace: str = "migrations", table: str = "migrations"):
        self.namespace = namespace
        self.table = table

    def init_remote(self):
        get_session().sql(f"CREATE NAMESPACE IF NOT EXISTS {self.namespace};")
        get_session().sql(
            f"CREATE TABLE {self.namespace}.{self.namespace} (version STRING);"
        )

    def remote_exists(self) -> bool:
        namespaces = [
            k["namespace"] for k in get_session().sql("SHOW NAMESPACES;").collect()
        ]
        return self.namespace in namespaces

    def update_remote(self, state: str):
        if state is None:
            state = "NULL"
        else:
            state = f'"{state}"'
        get_session().sql(
            f"INSERT OVERWRITE {self.namespace}.{self.table} VALUES ({state});"
        )

    def get_remote(self) -> str:
        version = (
            get_session()
            .read.format("iceberg")
            .load(f"{self.namespace}.{self.table}")
            .first()
        )
        if version:
            return version[0]

    def prepare_args(self) -> Tuple[Any]:
        return (get_session(),)


if __name__ == "__main__":
    app = init_app(IcebergEngine(), template=spark_template)
    app()
