#AnalizadorDeProyectos\run.py
import sys
import os

# Asegúrate de que el directorio `src` esté en el `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.application.main_app import run_app
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.infrastructure.file_ops_adapter import FileOpsAdapter
from src.infrastructure.content_manager_adapter import ContentManagerAdapter
from src.infrastructure.clipboard_adapter import ClipboardAdapter
from src.infrastructure.logger_adapter import LoggerAdapter

if __name__ == '__main__':
    repo_path = 'C:\\AppServ\\www\\AnalizadorDeProyecto'
    #updater = RepoUpdater(repo_path)
    #updater.run()
    try:
        file_manager_port = PythonFileManagerAdapter()
        file_ops_port = FileOpsAdapter(LoggerAdapter())
        content_manager_port = ContentManagerAdapter()
        clipboard_port = ClipboardAdapter()
        logger_port = LoggerAdapter()
        run_app(
            file_manager_port=file_manager_port,
            file_ops_port=file_ops_port,
            content_manager_port=content_manager_port,
            clipboard_port=clipboard_port,
            logger_port=logger_port
        )
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario. Saliendo del programa...")
