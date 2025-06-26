from abc import ABC, abstractmethod

class ContentManagerPort(ABC):
    @abstractmethod
    def asegurar_directorio_docs(self, path):
        pass
