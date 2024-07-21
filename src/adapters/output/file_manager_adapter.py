import os
import boto3
from config.settings import Settings
from ports.output.file_manager import FileManager

class FileManagerAdapter(FileManager):
    def __init__(self, aws_access_key_id=Settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY, region_name=Settings.AWS_REGION):
        if aws_access_key_id and aws_secret_access_key and region_name:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
        else:
            self.s3_client = None

    def rename_local(self, old_path, new_path):
        os.rename(old_path, new_path)
        return

    def rename_s3(self, bucket_name, source_key, dest_key):
        copy_source = {'Bucket': bucket_name, 'Key': source_key}
        self.s3_client.copy(copy_source, bucket_name, dest_key)

        self.s3_client.delete_object(Bucket=bucket_name, Key=source_key)

    def rename(self, source, dest, storage_type='LOCAL', bucket_name=None):
        if storage_type == 'S3' and self.s3_client:
            self.rename_s3(bucket_name, source, dest)
        else:
            self.rename_local(source, dest)