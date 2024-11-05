import boto3
import pyarrow.parquet as pq

from urllib.parse import urlparse
from io import BytesIO
from config.settings import Settings
from config.logging import logging
from ports.input.parquet_reader import ParquetReader


class S3ReaderAdapter(ParquetReader):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, aws_session_token):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            aws_session_token=aws_session_token,
        )

    def read(self, file, callback):
        chunk_size = 50000

        bucket_name = urlparse(file).netloc
        object_key = urlparse(file).path.lstrip('/')

        logging.info(f"Reading key '{object_key}' from bucket '{bucket_name}' ")

        obj = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = obj["Body"].read()

        with BytesIO(data) as data_stream:
            parquet_file = pq.ParquetFile(data_stream)

            for batch in parquet_file.iter_batches(batch_size=chunk_size):
                logging.info(f"Processing a chunk of size {chunk_size}")

                columns = {col: batch[col].to_pylist() for col in batch.schema.names}
                chunk_records = [dict(zip(columns, row)) for row in zip(*columns.values())]

                callback(chunk_records, file)

    def list_files(self, bucket_name, bucket_prefix=Settings.AWS_BUCKET_PREFIX):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name, Prefix=bucket_prefix
        )

        if Settings.REPROCESS:
            file_extension = ".parquet.processed"
        else:
            file_extension = ".parquet"

        parquet_files = []
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    if obj["Key"].endswith(file_extension):
                        key = obj.get("Key")
                        billing_period = self.extract_billing_period(key)
                        parquet_files.append((f"s3://{bucket_name}/{key}", billing_period))

        return parquet_files


    def extract_billing_period(self, file_path):

        parts = file_path.split('/')

        for part in parts:
            if 'BILLING_PERIOD=' in part:
                return part.split('=')[1]

        return None