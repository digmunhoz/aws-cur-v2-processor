
class Command:
    pass

class ProcessParquetFileCommand(Command):
    def __init__(self, file_path):
        self.file_path = file_path

class ValidateDataCommand(Command):
    def __init__(self, data):
        self.data = data

class TransformDataCommand(Command):
    def __init__(self, data):
        self.data = data
