import os
from prettyconf import config


class Settings:
    ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST", default="opensearch")
    ELASTICSEARCH_PORT = config("ELASTICSEARCH_PORT", default=9200)
    WORKER_THREADS = config("WORKER_THREADS", default=2, cast=eval)
    STORAGE_TYPE = config("STORAGE_TYPE", default="LOCAL")
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
    AWS_REGION = config("AWS_REGION", default="us-east-1")
    AWS_BUCKET_NAME = config("AWS_BUCKET_NAME", default="")
    REPROCESS = config("REPROCESS", default=False, cast=config.boolean)

    if STORAGE_TYPE == "S3":
        SOURCE_FILE = AWS_BUCKET_NAME
    else:
        SOURCE_FILE = "/tmp/parquet_files"