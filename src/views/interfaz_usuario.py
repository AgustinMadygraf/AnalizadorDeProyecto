# src/views/interfaz_usuario.py
class InterfazUsuario:
    def mostrar_menu(self):
        print("1. Listar Archivos")
        print("2. Salir")
        return input("Seleccione una opción: ")

    def mostrar_archivos(self, archivos):
        for archivo in archivos:
            print(archivo)
