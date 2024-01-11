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
    while True:
        print("\nOpciones:\n S - Salir\n R - Repetir con la misma ruta\n C - Cambiar la ruta\n H - Ayuda")
        opcion = input("Seleccione una opción [S/R/C/H]: ").upper()

        if opcion == 'S':
            exit()
        elif opcion == 'C':
            return 'C', solicitar_ruta()
        elif opcion == 'R':
            print("Repetir con la misma ruta.")
            return 'R', ruta_anterior
        elif opcion == 'H':
            mostrar_ayuda()
        else:
            print("Opción no válida. Por favor, elija una opción entre S, R, C y H.")
            
def mostrar_ayuda():
    print("\nAyuda del Analizador de Proyectos:")
    print(" S - Salir del programa.")
    print(" R - Repetir la operación con la misma ruta de carpeta.")
    print(" C - Cambiar la ruta de la carpeta para la operación.")
    print(" H - Mostrar este mensaje de ayuda.\n")

    
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
