from config.logging import logging

from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy import helpers
from ports.output.database_writer import DatabaseWriter
from config.settings import Settings


class OpensearchWriterAdapter(DatabaseWriter):
    def __init__(self, host="http://localhost", port=9200):
        self.es = OpenSearch(
            hosts=[{"host": host, "port": port}],
            connection_class=RequestsHttpConnection,
            pool_maxsize=10,
        )

    def setup_index_template(self):
        settings = {
            "priority": 0,
            "template": {
                "settings": {
                    "index.number_of_shards": "4",
                    "index.number_of_replicas": "0",
                    "index.refresh_interval": "1m",
                },
                "mappings": {
                    "properties": {},
                },
            },
            "index_patterns": [Settings.INDEX_PATTERN],
            "composed_of": [],
            "_meta": {"flow": "simple"},
        }
        try:
            logging.info(f"Setting Index Template: {Settings.INDEX_TEMPLATE}")
            self.es.indices.put_index_template(name=Settings.INDEX_TEMPLATE, body=settings)
        except Exception as e:
            logging.error(e)
            raise

    def write(self, data):
        try:
            self.setup_index_template()
            for success, info in helpers.parallel_bulk(
                self.es,
                data,
                thread_count=Settings.WORKER_THREADS,
                raise_on_error=False,
                raise_on_exception=False,
                chunk_size=200,
                queue_size=8,
            ):
                if not success:
                    logging.error(f"Failed to insert document: {info}")
                else:
                    logging.debug(f"Successfully inserted document: {info}")
            logging.info("Bulk insert operation completed")
        except Exception as e:
            logging.error(f"Exception during bulk insert operation: {e}", exc_info=True)
            raise
