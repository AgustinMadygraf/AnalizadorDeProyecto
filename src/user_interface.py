#AnalizadorDeProyectos\src\user_interface.py
from colorama import Fore, Style
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()



def menu_0():
    logger.info("Por favor, introduzca la ruta de la carpeta: ")
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

    logger.info("Por favor, seleccione una opción de configuración:")
    logger.info("0 - vacío")
    logger.info("1 - Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad")
    logger.info("2 - SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas")
    logger.info("3 - POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos")
    logger.info("4 - TODO.txt: Mejora de la Organización y Productividad en Proyectos de Software con todo.txt")
    logger.info("5 - Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas")
    print("")
    eleccion = input(f"{Fore.GREEN}Ingrese el número de la opción deseada: {Style.RESET_ALL}") or '0'
    # Validar la entrada del usuario y asegurarse de que sea una opción válida
    while eleccion not in opciones:
        logger.info("Opción no válida. Por defecto se seleccionará la opción 0.")
        eleccion = 0

    # Devolver el archivo de configuración basado en la selección del usuario
    archivo_seleccionado = opciones[eleccion]
    logger.info(f"Ha seleccionado la opción {eleccion}")
    print("")
    return archivo_seleccionado


