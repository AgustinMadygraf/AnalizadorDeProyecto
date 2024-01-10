# utilidades_sistema.py

import subprocess
import sys
from importlib import metadata

# Verificar e instalar librerías necesarias
def verificar_e_instalar_librerias(librerias):
    for libreria in librerias:
        try:
            metadata.version(libreria)
        except metadata.PackageNotFoundError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])

# Obtener versión de Python
def obtener_version_python():
    return sys.version

# Obtener librerías instaladas con pip
def obtener_librerias_pip():
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return resultado.stdout
