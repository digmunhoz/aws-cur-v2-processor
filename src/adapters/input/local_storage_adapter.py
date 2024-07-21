import glob
import pandas as pd
from ports.input.parquet_reader import ParquetReader


class LocalReaderAdapter(ParquetReader):
    def read(self, file_path):
        return pd.read_parquet(file_path).to_dict(orient="records")

    def list_files(self, directory_path):
        return glob.glob(rf"{directory_path}/*.parquet")
