# src/domain/i_file_manager.py

from abc import ABC, abstractmethod

class IFileManager(ABC):
    @abstractmethod
    def read_file(self, file_path):
        pass

    @abstractmethod
    def process_file(self, file_path):
        pass
