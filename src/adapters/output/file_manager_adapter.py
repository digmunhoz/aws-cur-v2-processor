import os
import boto3
from urllib.parse import urlparse
from config.settings import Settings
from config.logging import logging
from ports.output.file_manager import FileManager


class FileManagerAdapter(FileManager):
    def __init__(
        self,
        aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=Settings.AWS_SESSION_TOKEN,
        region_name=Settings.AWS_REGION,
    ):
        if aws_access_key_id and aws_secret_access_key and region_name:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=region_name,
            )
        else:
            self.s3_client = None

    def rename_local(self, file, suffix):
        new_name = file + suffix
        logging.info(f"Renaming file {file}")
        os.rename(file, new_name)
        return

    def rename_s3(self, file, suffix):
        bucket_name = urlparse(file).netloc
        source_key = urlparse(file).path.lstrip("/")
        dest_key = source_key + suffix

        copy_source = {"Bucket": bucket_name, "Key": source_key}
        logging.info(f"Renaming file {file}")
        self.s3_client.copy(copy_source, bucket_name, dest_key)

        logging.info(f"Deleteing file {file} after renaming")
        self.s3_client.delete_object(Bucket=bucket_name, Key=source_key)

    def rename(self, file, suffix, storage_type="LOCAL"):

        if storage_type == "S3" and self.s3_client:
            self.rename_s3(file, suffix)
        else:
            self.rename_local(file, suffix)
