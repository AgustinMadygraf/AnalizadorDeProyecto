from abc import ABC, abstractmethod

class ClipboardPort(ABC):
    @abstractmethod
    def copiar_contenido_al_portapapeles(self, nombre_archivo, extensiones_permitidas):
        pass
