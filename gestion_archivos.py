# gestion_archivos.py
import os
import datetime
import pyperclip


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
