# installer.py
import subprocess
import sys
from pathlib import Path
from src.logs.config_logger import configurar_logging
import winshell
import os
from win32com.client import Dispatch
from pathlib import Path


# Configuración del logger
logger = configurar_logging()

def crear_acceso_directo(ruta_archivo_bat, directorio_script):

    # Asumiendo que `directorio_script` ya es un objeto Path
    escritorio = Path(winshell.desktop())
    ruta_acceso_directo = escritorio / "AnalizadorDeProyecto.lnk"
    ruta_icono = directorio_script / "config" / "AnalizadorDeProyecto.ico"

    if not ruta_icono.is_file():
        logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
        return False


    if not os.path.isfile(ruta_icono):
        logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
        return False

    try:
        shell = Dispatch('WScript.Shell')
        acceso_directo = shell.CreateShortCut(ruta_acceso_directo)
        acceso_directo.Targetpath = str(ruta_archivo_bat)
        acceso_directo.WorkingDirectory = str(directorio_script)
        acceso_directo.IconLocation = str(ruta_icono)
        acceso_directo.save()
        logger.info(f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} exitosamente.")
        return True
    except OSError as e:
        logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error del sistema operativo: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Error inesperado al crear/actualizar el acceso directo: {e}", exc_info=True)
        return False


def main():
    directorio_script = Path(__file__).parent.resolve()
    limpieza_pantalla()
    logger.info("Iniciando instalador")

    # Crear archivo BAT que utiliza Pipenv
    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
    if not os.path.isfile(ruta_archivo_bat):
        logger.info("Creando archivo 'AnalizadorDeProyecto.bat'")
        crear_archivo_bat_con_pipenv(directorio_script, sys.executable)
    
    crear_acceso_directo(ruta_archivo_bat, directorio_script)

def crear_archivo_bat_con_pipenv(directorio_script, python_executable):
    ruta_main_py = os.path.join(directorio_script, 'src', 'main.py')
    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')

    # Ajustamos el contenido para ejecutar directamente main.py a través de pipenv
    contenido_bat = (
        "@echo off\n"
        "cd /d \"%~dp0\"\n"  # Cambia al directorio donde se encuentra el script .bat
        "pipenv run python \"{}\"\n".format(ruta_main_py) +  # Ejecuta main.py directamente
        "echo.\n"  # Agrega una línea en blanco al final de la ejecución
        "pause\n"  # Mantiene la ventana abierta para que puedas ver la salida del script
    )

    with open(ruta_archivo_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat)
    logger.info("Archivo 'AnalizadorDeProyecto.bat' creado exitosamente.")


def limpieza_pantalla():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info("Pantalla limpiada.")
    except Exception as e:
        logger.error(f"Error al limpiar la pantalla: {e}")

if __name__ == "__main__":
    main()
