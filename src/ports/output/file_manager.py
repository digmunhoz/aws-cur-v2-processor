from abc import ABC, abstractmethod

class FileManager(ABC):
    @abstractmethod
    def rename(self, old_file, new_file):
        pass