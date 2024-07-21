from abc import ABC, abstractmethod

class ParquetReader(ABC):
    @abstractmethod
    def read(self, path_or_bucket):
        pass

    @abstractmethod
    def list_files(self, path_or_bucket):
        pass
