from typing import Any, Tuple

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

from many import MigrationEngine, init_app
from many.templates import elasticsearch_template

es: Elasticsearch = None


def get_connection() -> Elasticsearch:
    global es
    if not es:
        es = connections.create_connection(host="localhost", port=9200)
    return es


class ElasticsearchEngine(MigrationEngine):
    def __init__(self, index: str = "migrations", _id: str = "state"):
        self.index = index
        self._id = _id

    def init_remote(self):
        get_connection().indices.create(
            index=self.index,
            body={
                "mappings": {
                    "properties": {
                        "version": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        }
                    }
                }
            },
        )
        get_connection().index(index=self.index, id=self._id, body={})

    def remote_exists(self) -> bool:
        return get_connection().indices.exists(index=self.index)

    def update_remote(self, state: str):
        get_connection().index(index=self.index, id=self._id, body={"version": state})

    def get_remote(self) -> str:
        response = get_connection().get(index=self.index, id=self._id)
        if response["_source"]:
            return response["_source"]["version"]

    def prepare_args(self) -> Tuple[Any]:
        return (get_connection(),)


if __name__ == "__main__":
    app = init_app(ElasticsearchEngine(), template=elasticsearch_template)
    app()
