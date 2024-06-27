# src/models/json_file_manager.py

import json
from src.models.i_file_manager import IFileManager

class JsonFileManager(IFileManager):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implement specific processing for JSON files if necessary
        return json.dumps(content, indent=4)
