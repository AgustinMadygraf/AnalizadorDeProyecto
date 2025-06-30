# src/presentation/cli_entry.py
"""
Punto de entrada CLI para AnalizadorDeProyecto.
Separa el parsing de argumentos y la interacción de usuario de la orquestación principal.
"""
import sys
import os
import argparse
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.infrastructure.file_ops_adapter import FileOpsAdapter
from src.infrastructure.content_manager_adapter import ContentManagerAdapter
from src.infrastructure.clipboard_adapter import ClipboardAdapter
from src.infrastructure.logger_adapter import LoggerAdapter
from src.infrastructure.event_handler_adapter import EventHandlerAdapter
from src.infrastructure.file_handler_factory_adapter import FileHandlerFactoryAdapter
from src.infrastructure.tools.vulture_adapter.find_references import VultureAdapter
from src.application.batch_api import analizar_y_generar_reporte
from src.application.main_app import run_app
from colorama import init

def crear_adaptadores():
    handler_factory = FileHandlerFactoryAdapter()
    file_manager_port = PythonFileManagerAdapter()
    logger_port = LoggerAdapter()
    logger_event_port = logger_port  # LoggerAdapter implementa ambos puertos
    file_ops_port = FileOpsAdapter(logger_port)
    content_manager_port = ContentManagerAdapter()
    clipboard_port = ClipboardAdapter()
    event_handler_port = EventHandlerAdapter(logger_port)
    vulture_port = VultureAdapter()
    return dict(
        handler_factory=handler_factory,
        file_manager_port=file_manager_port,
        logger_port=logger_port,
        logger_event_port=logger_event_port,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        event_handler_port=event_handler_port,
        vulture_port=vulture_port
    )

def main():
    from src.application.orchestrator import main_orchestrator
    adaptadores = crear_adaptadores()
    main_orchestrator(**adaptadores)

    parser = argparse.ArgumentParser(
        description='AnalizadorDeProyecto: analiza y documenta proyectos de software.',
        epilog='''\nEjemplos de uso:\n  python run.py --input ./mi_proyecto --output reporte.txt --modo completo --incluir-todo --no-interactive\n  python run.py  # modo interactivo clásico\n\nFlags:\n  --input, -i           Ruta del directorio o archivo a analizar (obligatorio en modo batch)\n  --output, -o          Ruta del archivo de salida (opcional)\n  --modo, -m            Modo de análisis (resumen o completo)\n  --incluir-todo        Incluir el archivo todo.txt en el análisis\n  --no-interactive      Ejecutar en modo batch/no interactivo\n  --run-vulture         Ejecutar análisis de código muerto con vulture\n  --help, -h            Mostrar esta ayuda y salir\n''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', '-i', help='Ruta del directorio o archivo a analizar')
    parser.add_argument('--output', '-o', help='Ruta del archivo de salida (opcional)')
    parser.add_argument('--modo', '-m', help='Modo de análisis (ej: resumen, completo)', default='resumen')
    parser.add_argument('--incluir-todo', action='store_true', help="Incluir 'todo.txt' en el análisis")
    parser.add_argument('--no-interactive', action='store_true', help='Ejecutar en modo batch/no interactivo')
    parser.add_argument('--no-color', action='store_true', help='Desactivar colores ANSI en la salida')
    parser.add_argument('--lang', help='Idioma de la interfaz (es|en). También configurable con ANALIZADOR_LANG.', default=None)
    parser.add_argument('--run-vulture', action='store_true', help='Ejecutar análisis de código muerto con vulture')
    parser.add_argument('--version', action='store_true', help='Mostrar la versión del programa y salir')
    parser.add_argument('--help-modo', action='store_true', help='Mostrar ayuda sobre los modos de análisis y salir')
    parser.add_argument('--help-optimizacion', action='store_true', help='Mostrar ayuda sobre el submenú de optimización y salir')
    args = parser.parse_args()

    if getattr(args, 'version', False):
        try:
            from src.__version__ import __version__
        except ImportError:
            __version__ = 'desconocida'
        print(f'AnalizadorDeProyecto versión {__version__}')
        sys.exit(0)

    if getattr(args, 'help_modo', False):
        print("""
[AYUDA] Modos de análisis:
  resumen   - Análisis rápido: estructura, archivos clave, dependencias principales.
  completo  - Análisis profundo: incluye métricas, dependencias, sugerencias de mejora y documentación generada.

Ejemplo:
  python run.py --input ./mi_proyecto --modo completo --no-interactive
""")
        sys.exit(0)

    if getattr(args, 'help_optimizacion', False):
        print("""
[AYUDA] Submenú de optimización:
  1. Optimizar movimientos: Reordena operaciones para mayor eficiencia.
  2. Reescalar dimensiones: Ajusta escalas de salida según parámetros.
  0. Cancelar: Vuelve al menú principal.

Acceso:
  Disponible tras seleccionar 'Optimización' en el menú principal interactivo.
""")
        sys.exit(0)

    # ...existing CLI logic from run.py...
    # (Se puede refactorizar aquí el cuerpo principal de run.py)

if __name__ == '__main__':
    main()
