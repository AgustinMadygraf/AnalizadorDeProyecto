#SCR/InterfazHM.py
import os
import time
from logs.config_logger import configurar_logging
from SCR.GestArch import copiar_contenido_al_portapapeles

# Configuración del logger
logger = configurar_logging()


def menu_0():
    logger.info("\n\nPor favor, introduzca la ruta de la carpeta: ")
    ruta = input().strip()
    return ruta

def menu_1():
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

def menu_2(modo_prompt, ruta): 
    instrucciones = [
        "Abra www.chat.openai.com",
        "Abajo en el centro, haga click derecho donde dice 'Message ChatGPT...'",
        "Haga click en 'pegar'",
        "Presione tecla 'Enter'",
        "Espere a que ChatGPT le haga una devolución",
        f"Mientras tanto, vaya a {ruta}/AMIS",
        "Haga doble click en '01-ProjectAnalysis.md'",
        "Copie la devolución de ChatGPT y pegue en '01-ProjectAnalysis.md'",
        "Guarde '01-ProjectAnalysis.md'"
    ]

    if modo_prompt == 'config\prompt_upd_0.md':
        while True:
            for instruccion in instrucciones:
                print(instruccion)
                input("Presione Enter para continuar...\n")

            menu_2_0 = input("¿Ya pudo realizar el procedimiento sugerido? (S/N): ").upper()
            if menu_2_0 == 'S':
                break
            print("Por favor, intente nuevamente el procedimiento o solicite asistencia.")

        while True:
            menu_2_1 = input("¿Está conforme con la respuesta de ChatGPT? (S/N): ").upper()
            if menu_2_1 == 'S':
                break
            prompt_menu2 = "Proporcioname las modificaciones necesarias teniendo en cuentas las sugerencias que me haz realizado"
            copiar_contenido_al_portapapeles(prompt_menu2)
            print(f"\n\nCopiado al portapapeles: {prompt_menu2} \n\n")
            print("Por favor pegue abajo en el centro, donde dice 'Message ChatGPT...' y luego presione enter")
            input("Presione Enter una vez haya pegado el texto y recibido una respuesta.\n")

        print("Ahora el siguiente paso es crear un diagrama de flujo")
        # Aquí puedes incluir más instrucciones relacionadas con la creación del diagrama de flujo

    else:
        input("Presione una tecla para salir")
