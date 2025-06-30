"""

"""
# pylint: disable=no-name-in-module

from src.interfaces.file_handler_factory_port import FileHandlerFactoryPort
from src.domain.python_file_manager import PythonFileManager
from src.domain.markdown_file_manager import MarkdownFileManager
from src.domain.json_file_manager import JsonFileManager
from src.infrastructure.file_handlers.html_file_handler import HtmlFileHandler
from src.infrastructure.file_handlers.css_file_handler import CssFileHandler
from src.infrastructure.file_handlers.js_file_handler import JsFileHandler
from src.infrastructure.file_handlers.php_file_handler import PhpFileHandler

# TODO: Revisar posible código muerto (vulture): clase 'FileHandlerFactoryAdapter' reportada como sin uso
class FileHandlerFactoryAdapter(FileHandlerFactoryPort):
    def __init__(self):
        self.handlers = {
            '.py': PythonFileManager(),
            '.md': MarkdownFileManager(),
            '.json': JsonFileManager(),
            '.html': HtmlFileHandler(),
            '.css': CssFileHandler(),
            '.js': JsFileHandler(),
            '.php': PhpFileHandler()
        }

    def get_handler(self, extension):
        return self.handlers.get(extension)
