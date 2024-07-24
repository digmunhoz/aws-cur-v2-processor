import glob
import pandas as pd

from config.settings import Settings
from config.logging import logging
from ports.input.parquet_reader import ParquetReader


class LocalReaderAdapter(ParquetReader):
    def read(self, file):
        logging.info(f"Reading file: {file} from storage 'LOCAL'")
        return pd.read_parquet(file).to_dict(orient="records")

    def list_files(self, directory_path):

        if Settings.REPROCESS:
            file_extension = ".parquet.processed"
        else:
            file_extension = ".parquet"

        return glob.glob(rf"{directory_path}/*{file_extension}")
