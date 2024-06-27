# src/file_handlers/file_handler.py
from abc import ABC, abstractmethod

class FileHandler(ABC):
    @abstractmethod
    def read_file(self, file_path):
        pass

    @abstractmethod
    def process_file(self, file_path):
        pass
