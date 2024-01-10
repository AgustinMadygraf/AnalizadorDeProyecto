# gestion_archivos.py

import os
import datetime
import pyperclip
import logging


carpetas_a_omitir = ["__pycache__/"]
logging.basicConfig(filename='gestion_archivos.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas.

    Parámetros:
    archivos (list of str): Lista de nombres de archivos a filtrar.
    extensiones (list of str): Extensiones para usar en el filtrado.

    Retorna:
    list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    archivos_filtrados = []
    for archivo in archivos:
        if any(archivo.endswith(ext) for ext in extensiones):
            archivos_filtrados.append(archivo)
    return archivos_filtrados

def listar_archivos(ruta, extensiones):
    try:
        archivos_json, archivos_sql, otros_archivos = [], [], []
        estructura = []

        for raiz, _, archivos in os.walk(ruta):
            if '.git' in raiz:
                continue

            nivel = raiz.replace(ruta, '').count(os.sep)
            indentacion = ' ' * 4 * nivel
            estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
            subindentacion = ' ' * 4 * (nivel + 1)

            archivos_en_raiz = [os.path.join(raiz, archivo) for archivo in archivos]
            archivos_filtrados = filtrar_archivos_por_extension(archivos_en_raiz, extensiones)

            for archivo in archivos_filtrados:
                estructura.append(f"{subindentacion}{os.path.basename(archivo)}")
                if archivo.endswith('.json'):
                    archivos_json.append(archivo)
                elif archivo.endswith('.sql'):
                    archivos_sql.append(archivo)
                else:
                    otros_archivos.append(archivo)

        archivos_encontrados = otros_archivos + archivos_sql + archivos_json
        return archivos_encontrados, estructura
    except Exception as e:
        logging.error(f"Error al listar archivos en {ruta}: {e}")
        return [], []


def escribir_contenido_archivo(archivo, archivo_txt):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            archivo_txt.write("\n\n```\n\n")
            archivo_txt.write(f"# {archivo}\n")
            archivo_txt.writelines(linea for linea in file if not linea.strip().startswith('#'))
    except Exception as e:
        logging.error(f"Error al escribir el contenido del archivo {archivo}: {e}")

def obtener_estructura_formato(estructura):
    # Inicializamos la estructura formateada con el directorio raíz
    estructura_formateada = [estructura[0]]

    for linea in estructura[1:]:
        nivel = linea.count(' ') // 4  # Calculamos el nivel de indentación
        if nivel == 0:
            estructura_formateada.append(linea)
        else:
            # Verificamos si la línea contiene una carpeta a omitir
            omitir = any(carpeta in linea for carpeta in carpetas_a_omitir)
            if not omitir:
                # Agregamos la línea formateada con ramas para mostrar la jerarquía
                estructura_formateada.append("│   " * (nivel - 1) + "└── " + linea.strip())


    # Unimos las líneas formateadas en un solo texto
    return '\n'.join(estructura_formateada)

def generar_archivo_salida(ruta, archivos, estructura,modo_prompt):
    try:
        nombre = os.path.basename(os.path.normpath(ruta))
        nombre_archivo_salida = os.path.join(ruta, f"listado_{nombre}.txt")
        
        # Leer el contenido de prompt_mejora.txt
        ruta_directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo_prompt = os.path.join(ruta_directorio_actual, modo_prompt)
        with open(ruta_archivo_prompt, 'r', encoding='utf-8') as archivo_prompt:
            contenido_prompt = archivo_prompt.read()

        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_txt:
            fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo_txt.write(f"Fecha y hora de generación: {fecha_hora_actual}\n\n")
            archivo_txt.write(contenido_prompt + "\n\n")  
            archivo_txt.write("\n\nEstructura de Carpetas y Archivos:\n")
            
            # Utilizamos la función obtener_estructura_formato
            estructura_formateada = obtener_estructura_formato(estructura)
            archivo_txt.write(estructura_formateada + "\n\n")
            
            archivo_txt.write("Contenido de Archivos:\n")
            for archivo in archivos:
                escribir_contenido_archivo(archivo, archivo_txt)
        copiar_contenido_al_portapapeles(nombre_archivo_salida)
        return nombre_archivo_salida
    except Exception as e:
        logging.error(f"Error al generar el archivo de salida en {ruta}: {e}")
        return None

def copiar_contenido_al_portapapeles(nombre_archivo_salida):
    try:
        with open(nombre_archivo_salida, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        pyperclip.copy(contenido)
        logging.info(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")
    except Exception as e:
        logging.error(f"Error al copiar al portapapeles el archivo {nombre_archivo_salida}: {e}")
