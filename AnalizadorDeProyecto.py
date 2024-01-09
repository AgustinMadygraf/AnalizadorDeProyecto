import os
import sys
import datetime
import subprocess
import pyperclip
from importlib import metadata


# Verificar e instalar librerías necesarias
def verificar_e_instalar_librerias(librerias):
    for libreria in librerias:
        try:
            metadata.version(libreria)
        except metadata.PackageNotFoundError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])


# Obtener versión de Python
def obtener_version_python():
    return sys.version

# Obtener librerías instaladas con pip
def obtener_librerias_pip():
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return resultado.stdout

# Obtener ruta del archivo default
def obtener_ruta_default():
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    archivo_default = os.path.join(ruta_script, 'default.txt')
    if not os.path.exists(archivo_default):
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write("Contenido por defecto o dejar esta línea en blanco")
    with open(archivo_default, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Listar archivos según extensiones
def listar_archivos(ruta, extensiones):
    archivos_json, archivos_sql, otros_archivos = [], [], []
    estructura = []

    for raiz, _, archivos in os.walk(ruta):
        if '.git' in raiz:
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        indentacion = ' ' * 4 * nivel
        estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
        subindentacion = ' ' * 4 * (nivel + 1)

        for archivo in archivos:
            if archivo.endswith('.json'):
                archivos_json.append(os.path.join(raiz, archivo))
            elif archivo.endswith('.sql'):
                archivos_sql.append(os.path.join(raiz, archivo))
            elif any(archivo.endswith(ext) for ext in extensiones):
                otros_archivos.append(os.path.join(raiz, archivo))
            if archivo in archivos_json or archivo in archivos_sql or any(archivo.endswith(ext) for ext in extensiones):
                estructura.append(f"{subindentacion}{archivo}")

    archivos_encontrados = otros_archivos + archivos_sql + archivos_json
    return archivos_encontrados, estructura


# Escribir contenido de archivos en archivo de salida
def escribir_contenido_archivo(archivo, archivo_txt):
    with open(archivo, 'r', encoding='utf-8') as file:
        archivo_txt.write("\n\n#-------------------------------------------------------------------------\n")
        archivo_txt.write(f"# {archivo}\n")
        archivo_txt.writelines(linea for linea in file if not linea.strip().startswith('#'))

# Generar archivo de salida con listado de archivos
def generar_archivo_salida(ruta, archivos, estructura):
    nombre = os.path.basename(os.path.normpath(ruta))
    nombre_archivo_salida = os.path.join(ruta, f"listado_{nombre}.txt")
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_txt:
        fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo_txt.write(f"Fecha y hora de generación: {fecha_hora_actual}\n\n")
        archivo_txt.write("/start \nEres un experto en programación.\nAnaliza el siguiente proyecto, proporioname una sola sugerencia de mejora de buenas prácticas y un plan de acción para implementar dicha sugerencia\n\n")
        archivo_txt.write("\n\nEstructura de Carpetas y Archivos:\n")
        archivo_txt.writelines(f"{linea}\n" for linea in estructura)
        archivo_txt.write("\n\nContenido de Archivos:\n")
        for archivo in archivos:
            escribir_contenido_archivo(archivo, archivo_txt)
    copiar_contenido_al_portapapeles(nombre_archivo_salida)
    return nombre_archivo_salida

# Copiar contenido al portapapeles
def copiar_contenido_al_portapapeles(nombre_archivo_salida):
    with open(nombre_archivo_salida, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    pyperclip.copy(contenido)
    print(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")

# Solicitar ruta al usuario
def solicitar_ruta():
    return input("Ingrese la ruta de la carpeta: ")

# Función principal
def main():
    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql']
    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not os.path.isdir(ruta):
            print("La ruta proporcionada no es válida o no es accesible.")
            ruta_anterior = None
            continue
        nombre_archivo_salida = generar_archivo_salida(ruta, *listar_archivos(ruta, extensiones))
        if nombre_archivo_salida is None:
            print("No se generó ningún archivo.")
            ruta_anterior = None
            continue
        opcion = input("\n¿Desea salir (S), repetir con la misma ruta (R) o cambiar la ruta (C)? [S/R/C]: ").upper()
        if opcion == 'S':
            break
        elif opcion == 'C':
            input("Presione Enter para continuar...")
            ruta_anterior = solicitar_ruta()
        else:
            print("Repetir con la misma ruta.")
            ruta_anterior = ruta


def crear_archivo_bat():
    python_executable = sys.executable  # Ubicación del ejecutable de Python
    directorio_script = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
    ruta_script = os.path.join(directorio_script, 'listado_archivos_y_codigos.py')  # Ruta completa del script

    contenido_bat = f'@echo off\n"{python_executable}" "{ruta_script}"\npause\n'

    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
    with open(ruta_archivo_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat)

    print(f'Archivo .bat creado en: {ruta_archivo_bat}')

# Llamar a la función para crear el archivo .bat
crear_archivo_bat()

if __name__ == "__main__":
    main()
