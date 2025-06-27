# src/infrastructure/file_handlers/python_file_manager.py

from src.interfaces.i_file_manager import IFileManager

class PythonFileManager(IFileManager):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implement specific processing for Python files if necessary
        return content
