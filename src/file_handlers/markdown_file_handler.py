# src/file_handlers/markdown_file_handler.py
from src.file_handlers.file_handler import FileHandler

class MarkdownFileHandler(FileHandler):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implement specific processing for Markdown files
        return content
