import pandas as pd
from ports.input.parquet_reader import ParquetReader


class ParquetReaderAdapter(ParquetReader):
    def read(self, file_path):
        return pd.read_parquet(file_path).to_dict(orient="records")
