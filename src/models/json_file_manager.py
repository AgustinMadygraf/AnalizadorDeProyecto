# src/models/json_file_manager.py

import json
from src.models.i_file_manager import IFileManager
from src.logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class JsonFileManager(IFileManager):
    def validate_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json.load(file)
            logger.debug(f"Archivo JSON validado correctamente: {file_path}")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON en el archivo {file_path}: {e}")
            logger.debug(f"Contenido del archivo {file_path} inválido en línea {e.lineno}, columna {e.colno}: {e.msg}. Char: {e.pos}")
            return False
        except Exception as e:
            logger.error(f"Error desconocido al validar el archivo {file_path}: {e}")
            return False

    def read_file(self, file_path):
        if not self.validate_json(file_path):
            logger.error(f"El archivo {file_path} contiene JSON inválido. No se puede leer.")
            raise ValueError(f"El archivo {file_path} contiene JSON inválido.")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.debug(f"Archivo leído correctamente: {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error al leer el archivo {file_path}: {e}")
            logger.debug(f"Detalle del error: {str(e)}")
            raise

    def process_file(self, file_path):
        try:
            content = self.read_file(file_path)
            logger.debug(f"Archivo procesado correctamente: {file_path}")
            return json.dumps(content, indent=4)
        except ValueError as ve:
            logger.error(f"Error en process_file para el archivo {file_path}: {ve}")
            logger.debug(f"Detalle del error: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error desconocido en process_file para el archivo {file_path}: {e}")
            logger.debug(f"Detalle del error: {str(e)}")
            raise
