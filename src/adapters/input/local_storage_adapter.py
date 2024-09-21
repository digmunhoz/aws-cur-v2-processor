import pyarrow.parquet as pq
import glob

from config.settings import Settings
from config.logging import logging
from ports.input.parquet_reader import ParquetReader


class LocalReaderAdapter(ParquetReader):
    def read(self, file, callback):
        chunk_size=50000
        logging.info(f"Reading file: {file} from storage 'LOCAL' in chunks")

        with open(file, 'rb') as f:
            parquet_file = pq.ParquetFile(f)

            for batch in parquet_file.iter_batches(batch_size=chunk_size):
                logging.info(f"Processing a chunk of size {chunk_size}")

                columns = {col: batch[col].to_pylist() for col in batch.schema.names}
                chunk_records = [dict(zip(columns, row)) for row in zip(*columns.values())]

                callback(chunk_records, file)


    def list_files(self, directory_path):

        if Settings.REPROCESS:
            file_extension = ".parquet.processed"
        else:
            file_extension = ".parquet"

        return glob.glob(rf"{directory_path}/*{file_extension}")
