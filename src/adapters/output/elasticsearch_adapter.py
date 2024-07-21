from config.logging import logging

from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy import helpers
from ports.output.elasticsearch_writer import ElasticsearchWriter
from config.settings import Settings

class ElasticsearchWriterAdapter(ElasticsearchWriter):
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
                "mappings": {"properties": {}},
            },
            "index_patterns": ["aws-cur-v2*"],
            "composed_of": [],
            "_meta": {"flow": "simple"},
        }
        try:
            logging.info(f"Setting Index Template: cur-v2")
            self.es.indices.put_index_template(name="cur-v2", body=settings)
        except Exception as e:
            logging.error(e)

    def write(self, data):
        try:
            self.setup_index_template()
            for success, info in helpers.parallel_bulk(
                self.es,
                data,
                thread_count=Settings.WORKER_THREADS,
                raise_on_error=True,
                raise_on_exception=True,
                chunk_size=200,
                queue_size=8,
            ):
                if not success:
                    logging.error(info)
        except Exception as e:
            logging.error(e)
