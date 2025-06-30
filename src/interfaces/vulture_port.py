# Puerto para análisis de código muerto (VulturePort)
from abc import ABC, abstractmethod

class VulturePort(ABC):
    @abstractmethod
    def extract_names(self, source_dir: str) -> list:
        """Extrae nombres de funciones, clases y variables del código fuente."""
        pass

    @abstractmethod
    def find_references(self, name: str, search_dirs: list) -> list:
        """Busca referencias a un símbolo en el código fuente."""
        pass

    @abstractmethod
    def generate_removal_plan(self, report_path: str) -> list:
        """Genera un plan para eliminar código muerto detectado."""
        pass
