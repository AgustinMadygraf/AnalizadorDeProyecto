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
from src.infrastructure.event_handler_adapter import EventHandlerAdapter
from src.infrastructure.file_handler_factory_adapter import FileHandlerFactoryAdapter
from src.application.batch_api import analizar_y_generar_reporte
from colorama import init
from src.infrastructure.vulture.find_references import VultureAdapter

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
    parser.add_argument('--lang', help='Idioma de la interfaz (es|en). También configurable con ANALIZADOR_LANG.', default=None)
    args = parser.parse_args()

    # Detección automática de TTY o flag --no-color
    disable_colors = args.no_color or not sys.stdout.isatty()
    if disable_colors:
        os.environ['ANSI_COLORS_DISABLED'] = '1'
        # Parchea colorama para no usar colores
        try:
            init(strip=True)
        except ImportError:
            pass

    repo_path = os.path.dirname(os.path.abspath(__file__))
    try:
        # Inicialización de adaptadores concretos
        handler_factory_adapter = FileHandlerFactoryAdapter()
        file_manager_adapter = PythonFileManagerAdapter()
        logger_adapter = LoggerAdapter()
        file_ops_adapter = FileOpsAdapter(logger_adapter)
        content_manager_adapter = ContentManagerAdapter()
        clipboard_adapter = ClipboardAdapter()
        event_handler_adapter = EventHandlerAdapter(logger_adapter)
        vulture_adapter = VultureAdapter()

        # Determinar idioma
        lang = args.lang or os.environ.get('ANALIZADOR_LANG', 'es')
        MESSAGES = {
            'es': {
                'batch_done': '[INFO] Análisis batch finalizado.',
                'input_not_found': '[ERROR] Ruta de entrada no encontrada:',
                'input_suggestion': 'Sugerencia: Verifique que la ruta especificada con --input exista y sea accesible.',
                'batch_fail': '[ERROR] Fallo en el análisis:',
                'batch_fail_suggestion': 'Sugerencia: Revise los permisos de archivos y el formato de entrada.',
                'interrupted': '\nEjecución interrumpida por el usuario. Saliendo del programa...',
                'unexpected': '[ERROR] Error inesperado en modo interactivo:',
                'unexpected_suggestion': 'Sugerencia: Revise la configuración y reporte el error si persiste.'
            },
            'en': {
                'batch_done': '[INFO] Batch analysis completed.',
                'input_not_found': '[ERROR] Input path not found:',
                'input_suggestion': 'Tip: Check that the path specified with --input exists and is accessible.',
                'batch_fail': '[ERROR] Analysis failed:',
                'batch_fail_suggestion': 'Tip: Check file permissions and input format.',
                'interrupted': '\nExecution interrupted by user. Exiting...',
                'unexpected': '[ERROR] Unexpected error in interactive mode:',
                'unexpected_suggestion': 'Tip: Check configuration or report the error if it persists.'
            }
        }
        TXT = MESSAGES['en'] if lang == 'en' else MESSAGES['es']

        # Leer configuración por archivo .analizadorrc si existe
        import json
        config_defaults = {}
        config_path = os.path.join(os.path.dirname(__file__), '.analizadorrc')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_defaults = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[WARN] No se pudo leer .analizadorrc (JSON inválido): {e}")
            except OSError as e:
                print(f"[WARN] No se pudo acceder a .analizadorrc: {e}")
        # Sobrescribir args con valores de config si no se pasan por CLI
        for key, value in config_defaults.items():
            if getattr(args, key, None) in (None, False):
                setattr(args, key, value)

        # Validación estricta de argumentos obligatorios en modo batch
        if args.no_interactive:
            if not args.input:
                print(f"{TXT['input_not_found']} <stdin>")
                print(TXT['input_suggestion'])
                sys.exit(1)

        if args.no_interactive and args.input:
            # Soporte de entrada por stdin si --input es '-'
            if args.input == '-':
                import tempfile
                temp_input = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.tmp')
                for line in sys.stdin:
                    temp_input.write(line)
                temp_input.flush()
                temp_input.close()
                input_path = temp_input.name
            else:
                input_path = args.input
            try:
                analizar_y_generar_reporte(
                    ruta=input_path,
                    modo_prompt=args.modo,
                    project_path=repo_path,
                    incluir_todo=args.incluir_todo,
                    file_manager_port=file_manager_adapter,
                    file_ops_port=file_ops_adapter,
                    content_manager_port=content_manager_adapter,
                    clipboard_port=clipboard_adapter,
                    logger_port=logger_adapter,
                    event_handler_port=event_handler_adapter,
                    rapido=(args.modo.strip().lower() in ["rapido", "resumen", "estructura"]),
                    handler_factory=handler_factory_adapter
                )
                print(TXT['batch_done'])
                sys.exit(0)
            except FileNotFoundError as e:
                print(f"{TXT['input_not_found']} {e}")
                print(TXT['input_suggestion'])
                sys.exit(1)
            except (PermissionError, IsADirectoryError, OSError, ValueError) as e:
                print(f"{TXT['batch_fail']} {e}")
                print(TXT['batch_fail_suggestion'])
                sys.exit(2)
            except RuntimeError as e:
                # Log runtime errors and exit
                import traceback
                print(f"{TXT['batch_fail']} {e}")
                print(traceback.format_exc())
                print(TXT['batch_fail_suggestion'])
                sys.exit(2)
            except Exception as e:
                # Re-raise truly unexpected exceptions
                raise
        else:
            # Modo interactivo clásico
            run_app(
                file_manager_port=file_manager_adapter,
                file_ops_port=file_ops_adapter,
                content_manager_port=content_manager_adapter,
                clipboard_port=clipboard_adapter,
                logger_event_port=logger_adapter,
                event_handler_port=event_handler_adapter,
                handler_factory=handler_factory_adapter
            )
            sys.exit(0)
    except KeyboardInterrupt:
        print(TXT['interrupted'])
        sys.exit(130)

    # Ejemplo de uso de VultureAdapter (ajustar según integración real)
    # nombres = vulture_adapter.extract_names('src')
    # refs = vulture_adapter.find_references('nombre_funcion', ['src/domain', 'src/application'])
    # plan = vulture_adapter.generate_removal_plan('infrastructure/vulture/vulture_report.txt')
