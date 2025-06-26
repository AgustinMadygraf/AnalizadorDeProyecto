from abc import ABC, abstractmethod

class FileManagerPort(ABC):
    @abstractmethod
    def read_file(self, file_path):
        pass

    @abstractmethod
    def process_file(self, file_path):
        pass

    @abstractmethod
    def read_and_validate_file(self, file_path, permitir_lectura, extensiones_permitidas, validaciones_extras=None):
        pass
