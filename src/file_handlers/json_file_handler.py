# src/file_handlers/json_file_handler.py
import json
from src.file_handlers.file_handler import FileHandler

class JsonFileHandler(FileHandler):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implement specific processing for JSON files, if necessary
        return json.dumps(content, indent=4)
