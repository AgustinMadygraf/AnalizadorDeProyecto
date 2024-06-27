# src/file_utilities.py
import pyperclip
import os
from src.logs.config_logger import LoggerConfigurator
from src.models.file_manager import FileManager  # Importar la nueva clase

# Configuración del logger
logger = LoggerConfigurator().get_logger()
project_path = "C:\\AppServ\\www\\AnalizadorDeProyecto"

file_manager = FileManager(project_path)  # Crear una instancia de FileManager

def copiar_contenido_al_portapapeles(file_path_salida, extensiones_permitidas):
    if not os.path.exists(file_path_salida):
        logger.error(f"El archivo '{file_path_salida}' no existe.")
        return
    permitir_lectura = False
    contenido = file_manager.read_and_validate_file(file_path_salida, permitir_lectura, extensiones_permitidas)
    if contenido:
        try:
            pyperclip.copy(contenido)
            logger.info(f"El contenido del archivo ha sido copiado al portapapeles.")
        except pyperclip.PyperclipException as e:
            logger.error(f"No se pudo copiar al portapapeles: {e}")
    else:
        logger.warning(f"El archivo '{file_path_salida}' está vacío o no se pudo leer.")

def verificar_existencia_archivo(file_path):
    return os.path.exists(file_path)
