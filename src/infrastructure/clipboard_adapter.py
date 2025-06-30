from src.interfaces.clipboard_port import ClipboardPort
from src.infrastructure.file_utilities import copiar_contenido_al_portapapeles

# TODO: Revisar posible código muerto (vulture): clase 'ClipboardAdapter' y método 'paste' reportados como sin uso
class ClipboardAdapter(ClipboardPort):
    """
    Adaptador concreto que implementa el puerto ClipboardPort.
    Cumple Clean Architecture: la infraestructura implementa el puerto,
    la aplicación depende solo de la interfaz.
    """
    def copy(self, data: str) -> None:
        # Implementación mínima, usar utilitario si aplica
        # Aquí solo se deja un NotImplementedError si no hay lógica real
        raise NotImplementedError("Clipboard copy not implemented.")

    def paste(self) -> str:
        # Implementación mínima
        raise NotImplementedError("Clipboard paste not implemented.")

    def copiar_contenido_al_portapapeles(self, nombre_archivo, extensiones_permitidas):
        return copiar_contenido_al_portapapeles(nombre_archivo, extensiones_permitidas)
