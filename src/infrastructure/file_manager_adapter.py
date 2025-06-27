from src.interfaces.file_manager_port import FileManagerPort
import os
from src.infrastructure.logger_adapter import LoggerAdapter

# Adaptador: Implementación concreta de FileManager
# ...implementar aquí acceso a sistema de archivos, logging, etc...

class PythonFileManagerAdapter(FileManagerPort):
    def __init__(self, logger=None):
        self.logger = logger or LoggerAdapter()

    def read(self, path: str) -> str:
        return self.read_file(path)

    def write(self, path: str, content: str) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError as e:
            if self.logger:
                self.logger.warning(f"No se pudo leer el archivo '{file_path}' como UTF-8: {e}")
            return f"[AVISO: No se pudo leer el archivo '{file_path}' por error de codificación]"
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Error al leer el archivo '{file_path}': {e}")
            return f"[AVISO: No se pudo leer el archivo '{file_path}' por error inesperado]"

    def process_file(self, file_path):
        content = self.read_file(file_path)
        # Implementar procesamiento específico si es necesario
        return content

    def read_and_validate_file(self, file_path, permitir_lectura, extensiones_permitidas, validaciones_extras=None):
        if validaciones_extras is None:
            validaciones_extras = []
        # Validación simple: extensión permitida y archivo existe
        if not isinstance(file_path, str):
            return None
        if not os.path.isfile(file_path):
            return None
        if not any(file_path.endswith(ext) for ext in extensiones_permitidas):
            return None
        for validacion in validaciones_extras:
            if not validacion(file_path):
                return None
        return self.read_file(file_path)
