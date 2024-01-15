#SCR/InterfazHM.py
import os
import time
from logs.config_logger import configurar_logging
from GestArch import copiar_contenido_al_portapapeles

# Configuración del logger
logger = configurar_logging()


OPCIONES_MENU_1 = {
    1: 'config\prompt_upd_0.md',
    2: 'config\prompt_error.md',
    3: 'config\prompt_aprender.md'
}

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
    print("")
    mensaje = "Elige un modo \n\n1 - Implementar mejoras en la programación\n2- Solucionar errores\n3- Aprendizaje\n"
    return solicitar_opcion(mensaje, OPCIONES_MENU_1)

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
            print("")
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

        
        # Aquí puedes incluir más instrucciones relacionadas con la creación del diagrama de flujo

    else:
        input("Presione una tecla para salir")
def menu_3(modo_prompt, ruta):

    instrucciones = [
        f"Vaya a {ruta}\AMIS\\02-diagrama_flujo.txt",
        "Seleccione el contenido, copie",
        "Abra el navegador",
        "ingresa a https://flowchart.fun/ ",
        "Seleccione todo, borre",
        "Click derecho, pegar",
        "Listo, ya tiene el diagrama de flujo"
    ]

    if modo_prompt == 'config\prompt_upd_0.md':
        print("\nAhora el siguiente paso es crear un diagrama de flujo")
        while True:
            for instruccion in instrucciones:
                print(instruccion)
                input("Presione Enter para continuar...\n")

            menu_3_0 = input("¿Ya pudo realizar el procedimiento sugerido? (S/N): ").upper()
            if menu_3_0 == 'S':
                break
            print("Por favor, intente nuevamente el procedimiento o solicite asistencia.")


        # Aquí puedes incluir más instrucciones relacionadas con la creación del diagrama de flujo

    else:
        input("Presione una tecla para salir")