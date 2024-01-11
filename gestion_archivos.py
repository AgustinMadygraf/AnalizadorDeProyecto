# gestion_archivos.py
import pyperclip
import logging

logging.basicConfig(filename='logs/gestion_archivos.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def copiar_contenido_al_portapapeles(nombre_archivo_salida):
    try:
        with open(nombre_archivo_salida, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        pyperclip.copy(contenido)
        logging.info(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")
    except Exception as e:
        logging.error(f"Error al copiar al portapapeles el archivo {nombre_archivo_salida}: {e}")
