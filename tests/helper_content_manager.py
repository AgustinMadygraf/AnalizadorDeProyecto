import os

def contenido_archivo(archivos):
    """Devuelve el contenido de una lista de archivos."""
    resultado = ''
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            resultado += f"--- Contenido de {archivo} ---\n{contenido}\n"
        except Exception as e:
            resultado += f"Error al leer el archivo {archivo}: {e}\n"
    return resultado

def filtrar_archivos_por_extension(archivos, extensiones):
    """Filtra archivos por extensión."""
    return [f for f in archivos if os.path.splitext(f)[1] in extensiones]
