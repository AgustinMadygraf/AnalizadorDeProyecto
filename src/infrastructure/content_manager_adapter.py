from src.interfaces.content_manager_port import ContentManagerPort
from src.application.content_manager import asegurar_directorio_docs

class ContentManagerAdapter(ContentManagerPort):
    def load_content(self, source: str) -> str:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()

    def save_content(self, destination: str, content: str) -> None:
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(content)

    def asegurar_directorio_docs(self, path):
        return asegurar_directorio_docs(path)
