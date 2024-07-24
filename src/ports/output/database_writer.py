from abc import ABC, abstractmethod

class DatabaseWriter(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def setup_index_template(self, data):
        pass