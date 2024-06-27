# AnalizadorDeProyectos\src\path_manager.py

import datetime
import json
import os
from colorama import Fore, Style
from src.models.user_interface import UserInterface

ui = UserInterface()

from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()

def obtener_ruta_analisis(project_path, input_func=input):
    ruta_seleccionada = ui.obtener_ruta_default(input_func)  # Usa input_func aquí también
    if isinstance(ruta_seleccionada, dict):
        ruta_default = ruta_seleccionada['ruta']
    else:
        ruta_default = ruta_seleccionada  # En caso de que todavía soporte el formato antiguo

    logger.info(f"Directorio seleccionado: {ruta_default}\n")
    respuesta = input_func(f"{Fore.GREEN}¿Desea analizar el directorio? (S/N): {Style.RESET_ALL}").upper()
    print("")

    if respuesta == 'N':
        nueva_ruta = ui.menu_0()
        if nueva_ruta != ruta_default:
            ui.guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta

    return ruta_default

def crear_archivo_path_json():
    ui.crear_archivo_path_json()

def guardar_nueva_ruta_default(nueva_ruta):
    ui.guardar_nueva_ruta_default(nueva_ruta)

def obtener_ruta_script():
    return os.path.dirname(os.path.abspath(__file__))

def validar_ruta(ruta):
    if not ruta or not isinstance(ruta, str):
        logger.error(f"Validación de ruta fallida, la ruta proporcionada es inválida: '{ruta}'")
        return False

    es_directorio = os.path.isdir(ruta)
    es_accesible = os.access(ruta, os.R_OK)

    if not es_directorio or not es_accesible:
        logger.error(f"La ruta no es un directorio o no es accesible para lectura: '{ruta}'")
        return False

    return True

def seleccionar_ruta(project_path, input_func):
    ruta = obtener_ruta_analisis(project_path, input_func)
    return ruta

def seleccionar_modo_operacion(input_func=input):
    return ui.menu_1()
