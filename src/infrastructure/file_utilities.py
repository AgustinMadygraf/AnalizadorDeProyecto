# Migrated from src/file_utilities.py
# ...existing code from file_utilities.py will be placed here...
import os

def copiar_contenido_al_portapapeles(file_path_salida, extensiones_permitidas=None):
    """Copia el contenido de un archivo al portapapeles si existe y no está vacío."""
    if not os.path.exists(file_path_salida):
        print(f"El archivo '{file_path_salida}' no existe.")
        return
    with open(file_path_salida, 'r', encoding='utf-8') as f:
        contenido = f.read()
    if contenido:
        try:
            import pyperclip
            pyperclip.copy(contenido)
            print("El contenido del archivo ha sido copiado al portapapeles.")
        except Exception as e:
            print(f"No se pudo copiar al portapapeles: {e}")
    else:
        print(f"El archivo '{file_path_salida}' está vacío o no se pudo leer.")
