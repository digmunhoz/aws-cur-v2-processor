from abc import ABC, abstractmethod

class ParquetReader(ABC):
    @abstractmethod
    def read(self, file_path):
        pass
