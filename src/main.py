import glob
import concurrent.futures

from core.application.use_cases import ProcessParquetFile
from adapters.input.parquet_reader_adapter import ParquetReaderAdapter
from adapters.output.elasticsearch_adapter import ElasticsearchWriterAdapter
from adapters.output.file_manager_adapter import FileManagerAdapter
from core.domain.services import DataTransformer, DataValidator
from config.settings import Settings
from config.logging import logging


parquet_reader = ParquetReaderAdapter()
data_transformer = DataTransformer()
data_validator = DataValidator()
elasticsearch_writer = ElasticsearchWriterAdapter(
    host=Settings.ELASTICSEARCH_HOST, port=Settings.ELASTICSEARCH_PORT
)
file_manager = FileManagerAdapter()

process_parquet_file = ProcessParquetFile(
    parquet_reader, data_transformer, data_validator, elasticsearch_writer, file_manager
)


def run():
    logging.info("Starting CUR V2 Processor")
    files = glob.glob(rf"/tmp/parquet_files/*.parquet")

    if not files:
        logging.info("There is no file to process")
    else:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=Settings.FILE_THREADS
        ) as executor:
            futures = {
                executor.submit(process_parquet_file.execute, file): file
                for file in files
            }

            for future in concurrent.futures.as_completed(futures):
                file = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing file {file}: {e}")

    logging.info("Stopping CUR V2 Processor")


if __name__ == "__main__":
    run()
