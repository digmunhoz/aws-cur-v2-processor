import os

from config.logging import logging
from abc import ABC, abstractmethod

class FileManager(ABC):
    @abstractmethod
    def rename(self, old_file, new_file):
        logging.info(f"Renaming file {old_file}")
        os.rename(old_file, new_file)