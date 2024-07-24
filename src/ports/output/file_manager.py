from abc import ABC, abstractmethod

class FileManager(ABC):
    @abstractmethod
    def rename(self, file, suffix):
        pass