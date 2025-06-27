#AnalizadorDeProyectos\run.py
import sys
import os

# 1. Asegura que 'src' esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Importa solo adaptadores concretos para inyección de dependencias
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.infrastructure.file_ops_adapter import FileOpsAdapter
from src.infrastructure.content_manager_adapter import ContentManagerAdapter
from src.infrastructure.clipboard_adapter import ClipboardAdapter
from src.infrastructure.logger_adapter import LoggerAdapter

# 3. Importa la función de orquestación principal (no importa puertos aquí)
from src.application.main_app import run_app

# 4. Orquestación de dependencias: la infraestructura crea adaptadores y los inyecta a la aplicación
if __name__ == '__main__':
    repo_path = 'C:\\AppServ\\www\\AnalizadorDeProyecto'
    try:
        # Inicialización de adaptadores concretos
        file_manager_adapter = PythonFileManagerAdapter()
        logger_adapter = LoggerAdapter()
        file_ops_adapter = FileOpsAdapter(logger_adapter)
        content_manager_adapter = ContentManagerAdapter()
        clipboard_adapter = ClipboardAdapter()
        # Inyección de dependencias: solo puertos/interfaces en la lógica interna
        def event_handler(event):
            level = event.get('level')
            message = event.get('message')
            if level == 'debug':
                logger_adapter.debug(message)
            elif level == 'info':
                logger_adapter.info(message)
            elif level == 'warning':
                logger_adapter.warning(message)
            elif level == 'error':
                logger_adapter.error(message)
        run_app(
            file_manager_port=file_manager_adapter,
            file_ops_port=file_ops_adapter,
            content_manager_port=content_manager_adapter,
            clipboard_port=clipboard_adapter,
            event_handler=event_handler
        )
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario. Saliendo del programa...")
