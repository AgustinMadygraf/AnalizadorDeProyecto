# utilidades_sistema.py

import subprocess
import sys
from importlib import metadata

def verificar_e_instalar_librerias(librerias):
    for libreria in librerias:
        try:
            version_instalada = metadata.version(libreria)
            print(f"Librería '{libreria}' está instalada (versión {version_instalada}).")
        except metadata.PackageNotFoundError:
            print(f"Librería '{libreria}' no está instalada. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
            print(f"Librería '{libreria}' ha sido instalada.")
# Obtener versión de Python
def obtener_version_python():
    return sys.version

# Obtener librerías instaladas con pip
def obtener_librerias_pip():
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return resultado.stdout
