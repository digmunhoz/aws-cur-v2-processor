import os
from ports.output.file_manager import FileManager

class FileManagerAdapter(FileManager):
    def rename(self, old_path, new_path):
        os.rename(old_path, new_path)
        return