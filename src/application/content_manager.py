# Migrated from src/content_manager.py
# ...existing code from content_manager.py will be placed here...

import os

def asegurar_directorio_docs(path):
    """Crea el directorio de documentación si no existe."""
    docs_dir = os.path.join(path, 'docs')
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

# Stubs para compatibilidad con tests y otros imports

def contenido_archivo(path):
    """Stub: Devuelve el contenido de un archivo."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def filtrar_archivos_por_extension(archivos, extensiones):
    """Stub: Filtra archivos por extensión."""
    return [f for f in archivos if os.path.splitext(f)[1] in extensiones]
