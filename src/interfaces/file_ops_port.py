from abc import ABC, abstractmethod

class FileOpsPort(ABC):
    @abstractmethod
    def listar_archivos(self, path, extensiones_permitidas):
        pass
