from config.logging import logging
from config.settings import Settings


class ProcessParquetFile:
    def __init__(
        self,
        local_reader,
        s3_reader,
        data_transformer,
        data_validator,
        elasticsearch_writer,
        file_manager,
        storage_type,
    ):
        self.local_reader = local_reader
        self.s3_reader = s3_reader
        self.data_transformer = data_transformer
        self.data_validator = data_validator
        self.elasticsearch_writer = elasticsearch_writer
        self.file_manager = file_manager
        self.storage_type = storage_type

    def execute(self, path_or_bucket):

        if self.storage_type == "S3":
            files = self.s3_reader.list_files(path_or_bucket)
            for file in files:
                logging.info(f"Reading file: s3://{path_or_bucket}/{file} from storage '{self.storage_type}'")
                data = self.s3_reader.read(path_or_bucket, file)
                self._process_data(data, file, bucket_name=path_or_bucket)
        else:
            files = self.local_reader.list_files(path_or_bucket)
            for file in files:
                logging.info(f"Reading file: {file} from storage '{self.storage_type}'")
                data = self.local_reader.read(file)
                self._process_data(data, file)

    def _process_data(self, data, source, bucket_name=None):
        if not self.data_validator.validate(data):
            raise ValueError("Invalid data")

        logging.info(f"Transforming file: {source}")
        transformed_data = self.data_transformer.transform(data)

        logging.info(f"Writing file: {source} into elasticsearch")
        self.elasticsearch_writer.write(transformed_data)

        if not Settings.REPROCESS:
            logging.info(f"Renaming file {source}")
            processed_file_path = source + ".processed"
            self.file_manager.rename(source, processed_file_path, self.storage_type, bucket_name)


class ValidateData:
    def __init__(self, validator):
        self.validator = validator

    def execute(self, data):
        return self.validator.validate(data)


class TransformData:
    def __init__(self, transformer):
        self.transformer = transformer

    def execute(self, data):
        return self.transformer.transform(data)
