#AnalizadorDeProyectos\run.py
import sys
import os
import argparse

# 1. Asegura que 'src' esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Importa solo adaptadores concretos para inyección de dependencias
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.infrastructure.file_ops_adapter import FileOpsAdapter
from src.infrastructure.content_manager_adapter import ContentManagerAdapter
from src.infrastructure.clipboard_adapter import ClipboardAdapter
from src.infrastructure.logger_adapter import LoggerAdapter
from src.application.batch_api import analizar_y_generar_reporte

# 3. Importa la función de orquestación principal (no importa puertos aquí)
from src.application.main_app import run_app

# 4. Orquestación de dependencias: la infraestructura crea adaptadores y los inyecta a la aplicación
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AnalizadorDeProyecto: analiza y documenta proyectos de software.',
        epilog='''\nEjemplos de uso:\n  python run.py --input ./mi_proyecto --output reporte.txt --modo completo --incluir-todo --no-interactive\n  python run.py  # modo interactivo clásico\n\nFlags:\n  --input, -i           Ruta del directorio o archivo a analizar (obligatorio en modo batch)\n  --output, -o          Ruta del archivo de salida (opcional)\n  --modo, -m            Modo de análisis (resumen o completo)\n  --incluir-todo        Incluir el archivo todo.txt en el análisis\n  --no-interactive      Ejecutar en modo batch/no interactivo\n  --help, -h            Mostrar esta ayuda y salir\n''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', '-i', help='Ruta del directorio o archivo a analizar')
    parser.add_argument('--output', '-o', help='Ruta del archivo de salida (opcional)')
    parser.add_argument('--modo', '-m', help='Modo de análisis (ej: resumen, completo)', default='resumen')
    parser.add_argument('--incluir-todo', action='store_true', help="Incluir 'todo.txt' en el análisis")
    parser.add_argument('--no-interactive', action='store_true', help='Ejecutar en modo batch/no interactivo')
    parser.add_argument('--no-color', action='store_true', help='Desactivar colores ANSI en la salida')
    args = parser.parse_args()

    # Detección automática de TTY o flag --no-color
    disable_colors = args.no_color or not sys.stdout.isatty()
    if disable_colors:
        import os
        os.environ['ANSI_COLORS_DISABLED'] = '1'
        # Parchea colorama para no usar colores
        try:
            from colorama import init, AnsiToWin32
            init(strip=True)
        except ImportError:
            pass

    repo_path = os.path.dirname(os.path.abspath(__file__))
    try:
        # Inicialización de adaptadores concretos
        file_manager_adapter = PythonFileManagerAdapter()
        logger_adapter = LoggerAdapter()
        file_ops_adapter = FileOpsAdapter(logger_adapter)
        content_manager_adapter = ContentManagerAdapter()
        clipboard_adapter = ClipboardAdapter()
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

        if args.no_interactive and args.input:
            # Modo batch/no interactivo
            try:
                analizar_y_generar_reporte(
                    ruta=args.input,
                    modo_prompt=args.modo,
                    project_path=repo_path,
                    incluir_todo=args.incluir_todo,
                    file_manager_port=file_manager_adapter,
                    file_ops_port=file_ops_adapter,
                    content_manager_port=content_manager_adapter,
                    clipboard_port=clipboard_adapter,
                    event_handler=event_handler
                )
                print("[INFO] Análisis batch finalizado.")
                sys.exit(0)
            except FileNotFoundError as e:
                print(f"[ERROR] Ruta de entrada no encontrada: {e}")
                print("Sugerencia: Verifique que la ruta especificada con --input exista y sea accesible.")
                sys.exit(1)
            except Exception as e:
                print(f"[ERROR] Fallo en el análisis: {e}")
                print("Sugerencia: Revise los permisos de archivos y el formato de entrada.")
                sys.exit(2)
        else:
            # Modo interactivo clásico
            run_app(
                file_manager_port=file_manager_adapter,
                file_ops_port=file_ops_adapter,
                content_manager_port=content_manager_adapter,
                clipboard_port=clipboard_adapter,
                event_handler=event_handler
            )
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario. Saliendo del programa...")
