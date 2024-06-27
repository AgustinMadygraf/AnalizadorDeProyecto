# src/models/markdown_file_manager.py

from src.models.i_file_manager import IFileManager

class MarkdownFileManager(IFileManager):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implement specific processing for Markdown files if necessary
        return content
