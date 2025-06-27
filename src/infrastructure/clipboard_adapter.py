from src.interfaces.clipboard_port import ClipboardPort
from src.infrastructure.file_utilities import copiar_contenido_al_portapapeles

class ClipboardAdapter(ClipboardPort):
    def copiar_contenido_al_portapapeles(self, nombre_archivo, extensiones_permitidas):
        return copiar_contenido_al_portapapeles(nombre_archivo, extensiones_permitidas)
