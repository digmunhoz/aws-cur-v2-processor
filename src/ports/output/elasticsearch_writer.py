from abc import ABC, abstractmethod

class ElasticsearchWriter(ABC):
    @abstractmethod
    def write(self, data):
        pass
