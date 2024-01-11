# interfaz_usuario.py
import logging


def solicitar_ruta():
    return input("Ingrese la ruta de la carpeta: ")

def mostrar_opciones(ruta_anterior):
    opcion = input("\n¿Desea salir (S), repetir con la misma ruta (R) o cambiar la ruta (C)? [S/R/C]: ").upper()
    if opcion == 'S':
        exit()
    elif opcion == 'C':
        return 'C', solicitar_ruta()
    else:
        print("Repetir con la misma ruta.")
        return 'R', ruta_anterior
    

def elegir_modo():
    while True:
        try:
            opcion = int(input("Elige un modo (1 - Implementar mejoras en la programación, 2 - Solucionar errores, 3 - Implementar mejoras en la UX/UI): "))
            if opcion == 1:
                logging.info("Modo seleccionado: Implementar mejoras en la programación")
                return 'prompt_mejora.txt'
            elif opcion == 2:
                logging.info("Modo seleccionado: Solucionar errores")
                return 'prompt_error.txt'
            elif opcion == 3:
                logging.info("Modo seleccionado: Implementar mejoras en la UX/UI")
                return 'prompt_mejora_ui.txt'  
            else:
                logging.warning(f"Opción inválida ingresada: {opcion}")
                print("Opción no válida. Por favor, elija una opción entre 1 y 3.")
        except ValueError:
            logging.error("Error en la entrada: No se ingresó un número")
            print("Por favor, ingrese una opción válida.")
