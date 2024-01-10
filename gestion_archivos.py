# gestion_archivos.py

import os
import datetime
import pyperclip

carpetas_a_omitir = ["__pycache__/"]

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
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return [], []

def escribir_contenido_archivo(archivo, archivo_txt):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            archivo_txt.write("\n\n```\n\n")
            archivo_txt.write(f"# {archivo}\n")
            archivo_txt.writelines(linea for linea in file if not linea.strip().startswith('#'))
    except Exception as e:
        print(f"Error al escribir el contenido del archivo {archivo}: {e}")

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
        print(f"Error al generar el archivo de salida: {e}")
        return None

def copiar_contenido_al_portapapeles(nombre_archivo_salida):
    try:
        with open(nombre_archivo_salida, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        pyperclip.copy(contenido)
        print(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")
    except Exception as e:
        print(f"Error al copiar al portapapeles: {e}")
