from src.interfaces.content_manager_port import ContentManagerPort
from src.application.content_manager import asegurar_directorio_docs

# TODO: Revisar posible código muerto (vulture): clase 'ContentManagerAdapter', métodos 'load_content' y 'save_content' reportados como sin uso
class ContentManagerAdapter(ContentManagerPort):
    """
    Adaptador concreto que implementa el puerto ContentManagerPort.
    Cumple Clean Architecture: la infraestructura implementa el puerto,
    la aplicación depende solo de la interfaz.
    """
    def load_content(self, source: str) -> str:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()

    def save_content(self, destination: str, content: str) -> None:
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(content)

    def asegurar_directorio_docs(self, path):
        return asegurar_directorio_docs(path)
