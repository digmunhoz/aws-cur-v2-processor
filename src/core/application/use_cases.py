
from config.logging import logging


class ProcessParquetFile:
    def __init__(self, parquet_reader, data_transformer, data_validator, elasticsearch_writer, file_manager):
        self.parquet_reader = parquet_reader
        self.data_transformer = data_transformer
        self.data_validator = data_validator
        self.elasticsearch_writer = elasticsearch_writer
        self.file_manager = file_manager

    def execute(self, parquet_file_path):
        try:
            logging.info(f"Processing file: {parquet_file_path} into dataset")
            data = self.parquet_reader.read(parquet_file_path)

            if not self.data_validator.validate(data):
                raise ValueError("Invalid data")

            logging.info(f"Transforming file: {parquet_file_path}")
            transformed_data = self.data_transformer.transform(data)

            logging.info(f"Writing file: {parquet_file_path} into elasticsearch")
            self.elasticsearch_writer.write(transformed_data)

            logging.info(f"Renaming file {parquet_file_path}")
            processed_file_path = parquet_file_path + ".processed"
            self.file_manager.rename(parquet_file_path, processed_file_path)
        except Exception as e:
            logging.error(e)

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
