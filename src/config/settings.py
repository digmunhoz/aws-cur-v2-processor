import os
from prettyconf import config


class Settings:
    ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST", default="opensearch")
    ELASTICSEARCH_PORT = config("ELASTICSEARCH_PORT", default=9200)
    FILE_THREADS = config("FILE_THREADS", default=2)
    WORKER_THREADS = config("WORKER_THREADS", default=2)