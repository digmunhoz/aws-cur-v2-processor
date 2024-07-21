from core.application.use_cases import ProcessParquetFile
from adapters.input.local_storage_adapter import LocalReaderAdapter
from adapters.input.s3_storage_adapter import S3ReaderAdapter
from adapters.output.elasticsearch_adapter import ElasticsearchWriterAdapter
from adapters.output.file_manager_adapter import FileManagerAdapter
from core.domain.services import DataTransformer, DataValidator
from config.settings import Settings
from config.logging import logging


local_reader = LocalReaderAdapter()
s3_reader = S3ReaderAdapter(
    Settings.AWS_ACCESS_KEY_ID, Settings.AWS_SECRET_ACCESS_KEY, Settings.AWS_REGION
)
data_transformer = DataTransformer()
data_validator = DataValidator()
elasticsearch_writer = ElasticsearchWriterAdapter(
    host=Settings.ELASTICSEARCH_HOST, port=Settings.ELASTICSEARCH_PORT
)
file_manager = FileManagerAdapter()

process_parquet_files = ProcessParquetFile(
    local_reader,
    s3_reader,
    data_transformer,
    data_validator,
    elasticsearch_writer,
    file_manager,
    Settings.STORAGE_TYPE,
)


def run():
    logging.info("Starting CUR V2 Processor")
    process_parquet_files.execute(Settings.SOURCE_FILE)
    logging.info("Stopping CUR V2 Processor")


if __name__ == "__main__":
    run()
