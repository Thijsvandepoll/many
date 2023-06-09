from elasticsearch import Elasticsearch

version = ${repr(version)}
down_version = ${repr(down_version)}


def up(connection: Elasticsearch):
    # Insert your UP migration below
    ...


def down(connection: Elasticsearch):
    # Insert your DOWN migration below
    ...