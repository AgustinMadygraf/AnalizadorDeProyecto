# utilidades_sistema.py
import subprocess
import sys
from importlib import metadata
import logging
import os

logging.basicConfig(filename='logs/utilidades_sistema.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def verificar_e_instalar_librerias(librerias):
    for libreria in librerias:
        try:
            version_instalada = metadata.version(libreria)
            logging.info(f"Librería '{libreria}' está instalada (versión {version_instalada}).")
        except metadata.PackageNotFoundError:
            logging.warning(f"Librería '{libreria}' no está instalada. Instalando...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
                logging.info(f"Librería '{libreria}' ha sido instalada.")
            except Exception as e:
                logging.error(f"No se pudo instalar la librería '{libreria}': {e}")

def obtener_version_python():
    return sys.version

def obtener_librerias_pip():
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return resultado.stdout

def limpieza_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')