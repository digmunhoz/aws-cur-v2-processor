import sys

from core.application.use_cases import ProcessParquetFile
from adapters.input.local_storage_adapter import LocalReaderAdapter
from adapters.input.s3_storage_adapter import S3ReaderAdapter
from factories.input_adapter_factory import InputAdapterFactory
from factories.output_adapter_factory import OutputAdapterFactory
from adapters.output.file_manager_adapter import FileManagerAdapter
from core.domain.services import DataTransformer, DataValidator
from config.settings import Settings
from config.logging import logging


data_transformer = DataTransformer()
data_validator = DataValidator()
input_adapter = InputAdapterFactory.create_input_adapter()
output_adapter = OutputAdapterFactory.create_output_adapter()
file_manager = FileManagerAdapter()


process_parquet_files = ProcessParquetFile(
    input_adapter,
    data_transformer,
    data_validator,
    output_adapter,
    file_manager,
    Settings.STORAGE_TYPE,
)


def run():

    try:
        logging.info("Starting CUR V2 Processor")
        process_parquet_files.execute(Settings.SOURCE_FILE)
        logging.info("Stopping CUR V2 Processor")
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == "__main__":
    run()
