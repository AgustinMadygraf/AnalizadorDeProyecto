# interfaz_usuario.py
import os
import time
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def elegir_modo():
    logger.debug("Inicio de la selección del modo de operación.")
    while True:
        try:
            logger.info("Elige un modo (1 - Implementar mejoras en la programación, 2 - Solucionar errores, 3 - Aprendizaje): ")
            opcion_str = input("")  
            opcion = int(opcion_str)  

            if opcion == 1:
                logger.info("Modo seleccionado: Implementar mejoras en la programación.")
                time.sleep(1)
                print("")

                return 'config\prompt_upd_0.md'
            elif opcion == 2:
                logger.info("Modo seleccionado: Solucionar errores.")
                return 'config\prompt_error.md'
            elif opcion == 3:
                logger.info("Modo seleccionado: Aprendizaje.")
                return 'config\prompt_aprender.md'
            else:
                logger.warning("Opción no válida. Debes elegir 1, 2 o 3.")
                return 'config\prompt_upd_0.md'
        except ValueError:
            logger.warning("Entrada no válida. Debes ingresar un número.")
            continue


def menu_2(ruta_anterior): ############################################################################### MENU 2
    logger.info('Ahora deberá por medio de un LLM, como podría ser ChatGPT, pegar "control + V" y la devolución del LLM deberá copiarlo a continuación')
    time.sleep(3)
    logger.info("")
    input("")



def mostrar_ayuda():
    logger.info("Mostrando mensaje de ayuda")
    logger.info("\nAyuda del Analizador de Proyectos:")
    logger.info(" S - Salir del programa.")
    logger.info(" R - Repetir la operación con la misma ruta de carpeta.")
    logger.info(" C - Cambiar la ruta de la carpeta para la operación.")
    logger.info(" H - Mostrar este mensaje de ayuda.\n")

def solicitar_ruta():
    logger.info("\n\nPor favor, introduzca la ruta de la carpeta: ")
    ruta = input().strip()
    return ruta
