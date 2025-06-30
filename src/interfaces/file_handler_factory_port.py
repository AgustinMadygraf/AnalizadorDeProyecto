from abc import ABC, abstractmethod

class FileHandlerFactoryPort(ABC):
    @abstractmethod
    def get_handler(self, extension):
        """
        Devuelve el handler adecuado para la extensión dada.
        Si no existe handler, retorna None.
        """
        pass
