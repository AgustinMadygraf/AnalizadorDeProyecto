#AnalizadorDeProyectos\src\user_interface.py
import os
import time
from logs.config_logger import configurar_logging
from file_manager import copiar_contenido_al_portapapeles

# Configuración del logger
logger = configurar_logging()



def menu_0():
    logger.info("\n\nPor favor, introduzca la ruta de la carpeta: ")
    return input().strip()

def solicitar_opcion(mensaje, opciones):
    logger.debug("Inicio de la selección del modo de operación.")
    while True:
        logger.info(mensaje)
        try:
            opcion = int(input())
            if opcion in opciones:
                return opciones[opcion]
            else:
                logger.warning("Opción no válida. Intente de nuevo.")
        except ValueError:
            logger.warning("Entrada no válida. Debes ingresar un número.")

def menu_1():
    """
    Presenta al usuario un menú con cuatro opciones de configuración y devuelve el archivo de configuración seleccionado.
    """
    opciones = {
        '0': 'config\\prompt_0.md',
        '1': 'config\\prompt_1.md',
        '2': 'config\\prompt_2.md',
        '3': 'config\\prompt_3.md',
        '4': 'config\\prompt_4.md',
        '5': 'config\\prompt_5.md' 
    }

    print("Por favor, seleccione una opción de configuración:")
    print("0: Vacío")
    print("1: Scrum Master")
    print("2: Backend")
    print("3: Frontend")
    print("4: Data Engineer")
    print("5: Vision Artificial & ML Specialist")
    
    eleccion = input("Ingrese el número de la opción deseada (presione Enter para seleccionar 0): ") or '0'

    # Validar la entrada del usuario y asegurarse de que sea una opción válida
    while eleccion not in opciones:
        print("Opción no válida. Por defecto se seleccionará la opción 0.")
        eleccion = 0

    # Devolver el archivo de configuración basado en la selección del usuario
    archivo_seleccionado = opciones[eleccion]
    print(f"Ha seleccionado la opción {eleccion}: {archivo_seleccionado}")
    return archivo_seleccionado


