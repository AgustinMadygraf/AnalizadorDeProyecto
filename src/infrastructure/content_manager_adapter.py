from src.interfaces.content_manager_port import ContentManagerPort
from src.application.content_manager import asegurar_directorio_docs

class ContentManagerAdapter(ContentManagerPort):
    def asegurar_directorio_docs(self, path):
        return asegurar_directorio_docs(path)
