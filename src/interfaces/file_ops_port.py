from abc import ABC, abstractmethod

class FileOpsPort(ABC):
    @abstractmethod
    def listar_archivos(self, path, extensiones_permitidas):
        pass
    
    @abstractmethod
    def contar_lineas_codigo(self, file_path, extensiones_codigo):
        pass
