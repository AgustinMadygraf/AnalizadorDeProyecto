#AnaliszadorDeProyecto/src/path_manager.py
import datetime
import json
import os
from colorama import Fore, Style
from src.user_interface import menu_0, menu_1

from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()

def obtener_ruta_analisis(project_path, input_func=input):
    ruta_seleccionada = obtener_ruta_default(input_func)  # Usa input_func aquí también
    if isinstance(ruta_seleccionada, dict):
        ruta_default = ruta_seleccionada['ruta']
    else:
        ruta_default = ruta_seleccionada  # En caso de que todavía soporte el formato antiguo

    logger.info(f"Directorio seleccionado: {ruta_default}\n")
    respuesta = input_func(f"{Fore.GREEN}¿Desea analizar el directorio? (S/N): {Style.RESET_ALL}").upper()
    print("")

    if respuesta == 'N':
        nueva_ruta = menu_0()  # Solicita al usuario una nueva ruta
        if nueva_ruta != ruta_default:
            guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta

    return ruta_default

def crear_archivo_path_json():
    ruta_directorio = 'config'
    archivo_default = os.path.join(ruta_directorio, 'path.json')

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ultimo_acceso = datetime.datetime.now().isoformat()

    contenido_inicial = {
        "rutas": [
            {
                "ruta": project_path,
                "ultimo_acceso": ultimo_acceso
            }
        ]
    }

    if not os.path.exists(ruta_directorio):
        os.makedirs(ruta_directorio)
        logger.info(f"Directorio {ruta_directorio} creado.")

    try:
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(contenido_inicial, file, indent=4)
        logger.info(f"Archivo {archivo_default} creado con éxito. Ruta del proyecto y fecha/hora actuales añadidas.")
    except Exception as e:
        logger.error(f"No se pudo crear el archivo {archivo_default}: {e}")

def guardar_nueva_ruta_default(nueva_ruta):
    archivo_default = 'config/path.json'
    try:
        # Cargar el archivo JSON existente o crear uno nuevo si no existe
        if os.path.exists(archivo_default):
            with open(archivo_default, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {"rutas": []}
        
        # Buscar la ruta en el archivo. Si existe, actualizar el timestamp
        ruta_existente = next((item for item in data["rutas"] if item["ruta"] == nueva_ruta), None)
        if ruta_existente:
            ruta_existente["ultimo_acceso"] = datetime.datetime.now().isoformat()
        else:
            # Añadir la nueva ruta al principio de la lista con el timestamp actual
            data["rutas"].insert(0, {"ruta": nueva_ruta, "ultimo_acceso": datetime.datetime.now().isoformat()})
        
        # Guardar el archivo JSON actualizado
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        logger.info(f"Nueva ruta por defecto guardada: {nueva_ruta}")
    except Exception as e:
        logger.error(f"Error al guardar la nueva ruta por defecto: {e}")

def obtener_ruta_default(input_func=input):
    archivo_default = 'config/path.json'
    if not os.path.exists(archivo_default):
        logger.info(f"El archivo {archivo_default} no existe. Creando uno nuevo.")
        crear_archivo_path_json()  # Llamada a la nueva función para crear el archivo
    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rutas = data.get('rutas', [])
        
        if not rutas:
            nueva_ruta = input_func("No se encontraron rutas guardadas. Por favor, introduzca una nueva ruta: ").strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta

        # Presentar las rutas de manera más amigable
        for i, ruta_info in enumerate(rutas, start=1):
            ruta = ruta_info['ruta']
            ultimo_acceso = ruta_info['ultimo_acceso']
            # Formatea y muestra cada ruta y su último acceso de manera clara
            logger.info(f"{i}. Ruta: {ruta} - Último acceso: {ultimo_acceso}")

        # Opción para introducir una nueva ruta
        logger.info(f"{len(rutas)+1}. Introducir una nueva ruta")
        print("")

        while True:
            eleccion = input_func(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}").strip()
            if not eleccion:
                return rutas[0]['ruta']
            elif eleccion.isdigit() and 1 <= int(eleccion) <= len(rutas):
                return rutas[int(eleccion)-1]['ruta']
            elif eleccion == str(len(rutas) + 1):
                nueva_ruta = input_func("Introduzca la nueva ruta: ").strip()
                guardar_nueva_ruta_default(nueva_ruta)
                return nueva_ruta
            else:
                logger.warning("Opción no válida. Por favor, intente de nuevo.")
                print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.{Style.RESET_ALL}")

    except Exception as e:
        logger.error(f"Ocurrió un error: {e}")
    except FileNotFoundError:
        nueva_ruta = input_func("Por favor, introduzca una nueva ruta: ").strip()
        guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta

def obtener_ruta_script():
    """
    Obtiene la ruta del directorio del script actual.

    Utiliza la variable mágica '__file__' para obtener la ruta completa del script en ejecución
    y luego extrae el directorio que lo contiene. Es útil para construir rutas relativas a la
    ubicación del script, independientemente del directorio de trabajo actual.

    Returns:
        str: Ruta del directorio donde se encuentra el script actual.
    """
    return os.path.dirname(os.path.abspath(__file__))

def validar_ruta(ruta):
    """
    Verifica si la ruta proporcionada es un directorio y si es accesible para lectura.

    Args:
        ruta (str): La ruta del directorio a validar.

    Returns:
        bool: True si la ruta es un directorio y es accesible para lectura, False en caso contrario.
    """
    # Asegurarse de que 'ruta' no sea None y sea una cadena no vacía
    if not ruta or not isinstance(ruta, str):
        logger.error(f"Validación de ruta fallida, la ruta proporcionada es inválida: '{ruta}'")
        return False

    # Verifica si la ruta es un directorio
    es_directorio = os.path.isdir(ruta)

    # Verifica si el directorio es accesible para lectura
    es_accesible = os.access(ruta, os.R_OK)

    if not es_directorio or not es_accesible:
        logger.error(f"La ruta no es un directorio o no es accesible para lectura: '{ruta}'")
        return False

    return True

def seleccionar_ruta(project_path, input_func):
    ruta = obtener_ruta_analisis(project_path, input_func)
    return ruta

def seleccionar_modo_operacion(input_func=input):
    """
    Permite al usuario seleccionar el modo de operación y devuelve el prompt correspondiente.
    """
    return menu_1()
