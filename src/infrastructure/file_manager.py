# src/infrastructure/file_manager.py
import os
import fnmatch
from src.interfaces.i_file_manager import IFileManager
from src.infrastructure.file_adapters.python_file_manager import PythonFileManager
from src.infrastructure.file_adapters.markdown_file_manager import MarkdownFileManager
from src.infrastructure.file_adapters.json_file_manager import JsonFileManager
from src.infrastructure.file_adapters.html_file_handler import HtmlFileHandler
from src.infrastructure.file_adapters.css_file_handler import CssFileHandler
from src.infrastructure.file_adapters.js_file_handler import JsFileHandler
from src.infrastructure.file_adapters.php_file_handler import PhpFileHandler
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
            logger.warning(f"No hay handler para la extensión: {extension}")
            return None
