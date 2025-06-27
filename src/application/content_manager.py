# Migrated from src/content_manager.py
# ...existing code from content_manager.py will be placed here...

import os

def asegurar_directorio_docs(path):
    """Crea el directorio de documentación si no existe."""
    docs_dir = os.path.join(path, 'docs')
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
