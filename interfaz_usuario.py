# interfaz_usuario.py

def solicitar_ruta():
    return input("Ingrese la ruta de la carpeta: ")

def mostrar_opciones(ruta_anterior):
    opcion = input("\n¿Desea salir (S), repetir con la misma ruta (R) o cambiar la ruta (C)? [S/R/C]: ").upper()
    if opcion == 'S':
        return 'S', None
    elif opcion == 'C':
        return 'C', solicitar_ruta()
    else:
        print("Repetir con la misma ruta.")
        return 'R', ruta_anterior
