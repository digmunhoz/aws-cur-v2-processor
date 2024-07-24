import boto3
import pandas as pd
from urllib.parse import urlparse
from io import BytesIO
from config.settings import Settings
from config.logging import logging
from ports.input.parquet_reader import ParquetReader


class S3ReaderAdapter(ParquetReader):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def read(self, file):
        bucket_name = urlparse(file).netloc
        object_key = urlparse(file).path.lstrip('/')
        logging.info(f"Reading key '{object_key}' from bucket '{bucket_name}' ")
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = obj["Body"].read()
        df = pd.read_parquet(BytesIO(data))

        return df.to_dict(orient="records")

    def list_files(self, bucket_name):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name, Prefix="reports/monthly-reports/"
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
                        parquet_files.append(f"s3://{bucket_name}/{key}")

        return parquet_files
