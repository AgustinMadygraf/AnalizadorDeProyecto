# src/file_handlers/js_file_handler.py
from src.file_handlers.file_handler import FileHandler

class JsFileHandler(FileHandler):
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implementar procesamiento específico para archivos JS si es necesario
        return content
