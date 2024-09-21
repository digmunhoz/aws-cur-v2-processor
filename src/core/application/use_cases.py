from config.logging import logging
from config.settings import Settings


class ProcessParquetFile:
    def __init__(
        self,
        input_reader,
        data_transformer,
        data_validator,
        database_writer,
        file_manager,
        storage_type,
    ):
        self.input_reader = input_reader
        self.data_transformer = data_transformer
        self.data_validator = data_validator
        self.database_writer = database_writer
        self.file_manager = file_manager
        self.storage_type = storage_type

    def execute(self, path_or_bucket):

        try:
            self.pre_process_data()
            files = self.input_reader.list_files(path_or_bucket)
            for file in files:
                logging.info(f"Start reading file {file}")
                _ = self.input_reader.read(file, self._process_data)

                if not Settings.REPROCESS:
                    suffix = ".processed"
                    self.file_manager.rename(file, suffix, self.storage_type)

        except Exception as e:
            logging.error(e)
            raise

    def pre_process_data(self):
        logging.info(f"Setting Index Template: cur-v2")
        self.database_writer.setup_index_template()

    def _process_data(self, data, file):

        if not self.data_validator.validate(data):
            raise ValueError("Invalid data")

        logging.info(f"Transforming file: {file}")
        transformed_data = self.data_transformer.transform(data)

        logging.info(f"Writing file: {file} into elasticsearch")
        self.database_writer.write(transformed_data)


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
