# src/models/file_manager.py
import os
import fnmatch
from src.models.i_file_manager import IFileManager
from src.models.python_file_manager import PythonFileManager
from src.models.markdown_file_manager import MarkdownFileManager
from src.models.json_file_manager import JsonFileManager
from src.file_handlers.html_file_handler import HtmlFileHandler
from src.file_handlers.css_file_handler import CssFileHandler
from src.file_handlers.js_file_handler import JsFileHandler
from src.file_handlers.php_file_handler import PhpFileHandler
from src.logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class FileManager:
    def __init__(self, project_path):
        self.project_path = project_path
        self.gitignore_patterns = self._leer_gitignore()
        self.handlers = {
            '.py': PythonFileManager(),
            '.md': MarkdownFileManager(),
            '.json': JsonFileManager(),
            '.html': HtmlFileHandler(),
            '.css': CssFileHandler(),
            '.js': JsFileHandler(),
            '.php': PhpFileHandler()
        }

    def _leer_gitignore(self):
        gitignore_path = os.path.join(self.project_path, '.gitignore')
        patrones = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                patrones = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return patrones

    def esta_en_gitignore(self, ruta_archivo):
        ruta_rel = os.path.relpath(ruta_archivo, self.project_path)
        for pattern in self.gitignore_patterns:
            if fnmatch.fnmatch(ruta_rel, pattern):
                return True
        return False

    def read_file(self, file_path):
        extension = os.path.splitext(file_path)[1]
        handler = self.handlers.get(extension)
        if handler:
            return handler.read_file(file_path)
        else:
            logger.warning(f"No hay manejador para la extensión {extension}")
            return None

    def process_file(self, file_path):
        extension = os.path.splitext(file_path)[1]
        handler = self.handlers.get(extension)
        if handler:
            return handler.process_file(file_path)
        else:
            logger.warning(f"No hay manejador para la extensión {extension}")
            return None

    def validar_file_path(self, file_path):
        if not isinstance(file_path, str):
            logger.warning(f"Tipo de dato incorrecto para file_path: {type(file_path)}. Se esperaba una cadena (str).")
            return False
        return True

    def read_and_validate_file(self, file_path, permitir_lectura, extensiones_permitidas, validaciones_extras=[]):
        if not self.validar_file_path(file_path):
            return None
        if not self.es_archivo_valido(file_path, extensiones_permitidas, permitir_lectura, validaciones_extras):
            return None
        return self.read_file(file_path)

    def es_archivo_valido(self, file_path, extensiones_permitidas, permitir_lectura, validaciones_extras):
        if not os.path.isfile(file_path):
            return False
        if not self.archivo_permitido(file_path, extensiones_permitidas):
            logger.debug(f"Extensión de archivo no permitida para lectura: {file_path}")
            return False
        if permitir_lectura:
            if not self.es_acceso_permitido(file_path, validaciones_extras):
                return False
        return True

    def archivo_permitido(self, file_path, extensiones_permitidas):
        file_path_puro = os.path.basename(file_path)
        archivos_especificamente_permitidos = {'Pipfile', 'Pipfile.lock'}
        return file_path_puro in archivos_especificamente_permitidos or \
               any(file_path_puro.endswith(ext) for ext in extensiones_permitidas)

    def es_acceso_permitido(self, file_path, validaciones_extras):
        if '..' in os.path.abspath(file_path) or "docs" in file_path:
            logger.debug("Acceso a archivo fuera del directorio permitido o intento de leer archivo en directorio 'docs'.")
            return False
        if os.path.getsize(file_path) > 10240:
            logger.warning(f"El archivo '{file_path}' excede el tamaño máximo permitido de 10KB.")
            return False
        if self.esta_en_gitignore(file_path):
            logger.warning(f"El archivo '{file_path}' está listado en .gitignore y no será leído.")
            return False
        for validacion in validaciones_extras:
            if not validacion(file_path):
                return False
        return True
