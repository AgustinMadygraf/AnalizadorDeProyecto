# interfaz_usuario.py
import os

def solicitar_ruta():
    while True:
        ruta = input("Ingrese la ruta de la carpeta: ")
        if os.path.isdir(ruta):
            return ruta
        else:
            print("La ruta ingresada no es válida o no existe. Inténtelo de nuevo.")


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
            opcion = int(input("Elige un modo (1 - Implementar mejoras en la programación, 2 - Solucionar errores): "))
            if opcion == 2:
                return 'prompt_error.txt'
            else:
                return 'prompt_mejora.txt'
        except ValueError:
            return 'prompt_mejora.txt'
