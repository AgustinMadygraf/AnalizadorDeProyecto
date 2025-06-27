# Migrated from src/path_manager.py
# ...existing code from path_manager.py will be placed here...
import os
import json
from colorama import Fore, Style
from common.i18n import LANG

def seleccionar_ruta(project_path, input_func=input):
    """Muestra un menú de rutas recientes y permite introducir una nueva ruta."""
    archivo_default = 'config/path.json'
    rutas = []
    if os.path.exists(archivo_default):
        with open(archivo_default, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rutas = data.get('rutas', [])
    print(f"{Fore.GREEN}{LANG.get('recent_paths', 'Rutas recientes:')}{Style.RESET_ALL}")
    print(LANG.get('menu_option_0', '0. Introducir nueva ruta'))
    for i, ruta_info in enumerate(rutas, start=1):
        ruta = ruta_info['ruta']
        print(f"{i}. {ruta}")
    while True:
        eleccion = input_func(f"{Fore.GREEN}{LANG.get('prompt_select_option', 'Seleccione una opción: ')}{Style.RESET_ALL}").strip()
        if not eleccion:
            if rutas:
                return rutas[0]['ruta']
            else:
                continue
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(rutas):
            return rutas[int(eleccion)-1]['ruta']
        elif eleccion == '0':
            nueva_ruta = input_func(LANG.get('prompt_enter_new_path', 'Introduzca la nueva ruta: ')).strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta
        else:
            print(f"{Fore.RED}{LANG.get('error_invalid_option', 'Opción no válida. Por favor, intente de nuevo.')}{Style.RESET_ALL}")

def guardar_nueva_ruta_default(nueva_ruta):
    archivo_default = 'config/path.json'
    try:
        if os.path.exists(archivo_default):
            with open(archivo_default, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {"rutas": []}
        ruta_existente = next((item for item in data["rutas"] if item["ruta"] == nueva_ruta), None)
        import datetime
        if ruta_existente:
            ruta_existente["ultimo_acceso"] = datetime.datetime.now().isoformat()
        else:
            data["rutas"].insert(0, {"ruta": nueva_ruta, "ultimo_acceso": datetime.datetime.now().isoformat()})
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(LANG.get('error_save_path', f"Error al guardar la nueva ruta por defecto: {e}"))

def validar_ruta(ruta):
    """Valida si la ruta existe y es accesible."""
    import os
    return os.path.exists(ruta) and os.path.isdir(ruta)

def seleccionar_modo_operacion(input_func=input):
    print(LANG.get('prompt_select_mode', 'Selecciona el modo de operación:'))
    print(LANG.get('mode_option_1', '1. Análisis completo'))
    print(LANG.get('mode_option_2', '2. Análisis rápido'))
    opcion = input_func(LANG.get('prompt_mode_option', 'Opción (1/2): ')).strip()
    if opcion == '2':
        return 'rapido'
    elif opcion == '1':
        return 'completo'
    else:
        return opcion
