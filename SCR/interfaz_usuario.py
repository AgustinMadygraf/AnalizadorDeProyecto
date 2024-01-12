# interfaz_usuario.py
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def solicitar_ruta():
    while True:
        ruta = input("Ingrese la ruta de la carpeta: ")
        if os.path.isdir(ruta):
            logger.info(f"Ruta ingresada: {ruta}")
            return ruta
        else:
            logger.warning("La ruta ingresada no es válida o no existe.")

def mostrar_opciones(ruta_anterior):
    while True:
        logger.info("\n\nOpciones:\n S - Salir\n R - Repetir con la misma ruta\n C - Cambiar la ruta\n H - Ayuda\n")
        opcion = input("Seleccione una opción [S/R/C/H]: \n").upper()

        if opcion == 'S':
            logger.info("Opción seleccionada: Salir")
            exit()
        elif opcion == 'C':
            logger.info("Opción seleccionada: Cambiar la ruta")
            return 'C', solicitar_ruta()
        elif opcion == 'R':
            logger.info("Opción seleccionada: Repetir con la misma ruta")
            logger.info("Repetir con la misma ruta.")
            return 'R', ruta_anterior
        elif opcion == 'H':
            logger.info("Opción seleccionada: Ayuda")
            mostrar_ayuda()
        else:
            logger.warning("Opción no válida seleccionada")
            logger.info("Opción no válida. Por favor, elija una opción entre S, R, C y H.")

def mostrar_ayuda():
    logger.info("Mostrando mensaje de ayuda")
    logger.info("\nAyuda del Analizador de Proyectos:")
    logger.info(" S - Salir del programa.")
    logger.info(" R - Repetir la operación con la misma ruta de carpeta.")
    logger.info(" C - Cambiar la ruta de la carpeta para la operación.")
    logger.info(" H - Mostrar este mensaje de ayuda.\n")

def elegir_modo():
    logger.info("Inicio de la selección del modo de operación.")
    while True:
        try:
            logger.info("Elige un modo (1 - Implementar mejoras en la programación, 2 - Solucionar errores): ")
            opcion_str = 1##################################################################################
            #opcion_str = input("")  ########################################
            opcion = int(opcion_str)  

            if opcion == 1:
                logger.info("Modo seleccionado: Implementar mejoras en la programación.")
                return 'prompt_mejora.md'
            elif opcion == 2:
                logger.info("Modo seleccionado: Solucionar errores.")
                return 'prompt_error.md'
            else:
                logger.warning("Opción no válida. Debes elegir 1 o 2. Seleccionando modo por defecto: Mejoras en la programación.")
                return 'prompt_mejora.txt'
        except ValueError:
            logger.error("Entrada no válida. Debes ingresar un número. Seleccionando modo por defecto: Mejoras en la programación.")
            return 'prompt_mejora.txt'

