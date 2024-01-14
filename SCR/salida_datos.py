#salida_datos.py
import os
import datetime
from gestion_archivos import leer_archivo, copiar_contenido_al_portapapeles
from logs.config_logger import configurar_logging
import datetime

# Configuración del logger
logger = configurar_logging()

def generar_archivo_salida(ruta, archivos, estructura, modo_prompt, extensiones):
    """
    Genera el archivo de salida con la estructura dada.

    Args:
        ruta (str): Ruta del directorio donde se generará el archivo de salida.
        estructura (list): Estructura de directorios y archivos a incluir en el archivo de salida.
        modo_prompt (str): Modo seleccionado para la salida.
        extensiones (list of str): Extensiones para filtrar archivos.
    """
    archivos_encontrados, estructura_actualizada = listar_archivos(ruta, extensiones)
    nombre_archivo_salida = generar_nombre_archivo_salida(ruta)
    formatear_archivo_salida(nombre_archivo_salida)
    contenido = preparar_contenido_salida(estructura_actualizada, modo_prompt, archivos_encontrados)
    escribir_archivo_salida(nombre_archivo_salida, contenido)
    copiar_contenido_al_portapapeles(nombre_archivo_salida)
    return nombre_archivo_salida

def formatear_archivo_salida(nombre_archivo_salida):
    """
    Elimina el contenido del archivo de salida.

    Args:
        nombre_archivo_salida (str): Ruta del archivo cuyo contenido se eliminará.
    """
    try:
        # Abrir el archivo en modo de escritura, lo que borrará su contenido
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write('')  # Escribir un contenido vacío
        logger.info(f"El contenido de {nombre_archivo_salida} ha sido eliminado.")
    except Exception as e:
        logger.warning(f"Error al intentar formatear el archivo {nombre_archivo_salida}: {e}")


def preparar_contenido_salida(estructura, modo_prompt, archivos_seleccionados):
    logger.info("Preparando contenido de salida")
    ruta_proyecto2 = "C:\\AppServ\\www\\AnalizadorDeProyecto\\config"
    nombre_archivo = os.path.join(ruta_proyecto2, modo_prompt)
    contenido_prompt = leer_archivo(nombre_archivo)

    contenido = contenido_prompt if contenido_prompt else "\n\nprompt:\nNo hay prompt. falla.\n\n"

    # Encabezado para la estructura de carpetas y archivos
    contenido += "\n\n## Estructura de Carpetas y Archivos\n```bash\n"
    contenido += '\n'.join(estructura) + "\n```\n"

    # Sección para contenido de archivos seleccionados
    if archivos_seleccionados:
        contenido += "\n\n## Contenido de Archivos Seleccionados\n"
        for archivo in archivos_seleccionados:
            contenido_archivo = leer_archivo(archivo)
            if contenido_archivo:
                contenido += f"\n### {archivo}\n```plaintext\n"
                contenido += escapar_caracteres_md(contenido_archivo) + "\n```\n"
            else:
                logger.warning(f"No se pudo obtener el contenido del archivo: {archivo}")
    else:
        logger.warning("No se han proporcionado archivos seleccionados para incluir en el contenido")

    return contenido

def escapar_caracteres_md(texto):
    """
    Escapa caracteres especiales de Markdown en un texto.

    Args:
        texto (str): Texto a escapar.

    Returns:
        str: Texto con caracteres de Markdown escapados.
    """
    caracteres_a_escapar = ['*', '_', '`', '!', '[', ']', '(', ')']
    for char in caracteres_a_escapar:
        texto = texto.replace(char, f'\\{char}')
    return texto

def generar_nombre_archivo_salida(ruta, nombre_base='listado'):
    """
    Genera el nombre del archivo de salida basado en la ruta y un nombre base.

    Args:
        ruta (str): Ruta del directorio para el archivo de salida.
        nombre_base (str): Nombre base para el archivo de salida.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    # Formatear la ruta para el nombre del archivo
    ruta_formateada = ruta.replace("\\", "%").replace(":", "_")
    nombre_archivo_salida = f"LIST-{ruta_formateada}.md"
    return os.path.join(ruta, nombre_archivo_salida)

def escribir_archivo_salida(nombre_archivo, contenido):
    """
    Escribe el contenido dado en el archivo de salida especificado.

    Args:
        nombre_archivo (str): Ruta del archivo donde se escribirá el contenido.
        contenido (str): Contenido a escribir en el archivo.
    """
    if contenido is None:
        logger.error(f"Intento de escribir contenido 'None' en el archivo {nombre_archivo}")
        contenido = "Contenido no disponible o error al leer el archivo."

    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        logger.info(f"Archivo de salida generado: {nombre_archivo}")
    except Exception as e:
        logger.error(f"Error al escribir en el archivo de salida {nombre_archivo}: {e}")

def contenido_archivo(archivos_seleccionados):
    contenido_total = ""
    for archivo in archivos_seleccionados:
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                contenido = file.read()
                contenido_total += f"\n--- Contenido de {archivo} ---\n"
                contenido_total += contenido + "\n"
        except Exception as e:
            contenido_total += f"\nError al leer el archivo {archivo}: {e}\n"
    return contenido_total
    
def listar_archivos(ruta, extensiones):
    try:
        archivos_encontrados = []
        estructura = []

        for raiz, _, archivos in os.walk(ruta):
            if '.git' in raiz:  # Ignorar directorios .git
                continue

            nivel = raiz.replace(ruta, '').count(os.sep)
            indentacion = ' ' * 4 * nivel
            estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
            subindentacion = ' ' * 4 * (nivel + 1)

            archivos_en_raiz = [os.path.join(raiz, archivo) for archivo in archivos]
            archivos_filtrados = filtrar_archivos_por_extension(archivos_en_raiz, extensiones)
            estructura.extend(f"{subindentacion}{os.path.basename(archivo)}" for archivo in archivos_filtrados)
            archivos_encontrados.extend(archivos_filtrados)

        return archivos_encontrados, estructura
    except Exception as e:
        logger.error(f"Error al listar archivos en {ruta}: {e}")
        return [], []

def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas.

    Parámetros:
    archivos (list of str): Lista de nombres de archivos a filtrar.
    extensiones (list of str): Extensiones para usar en el filtrado.

    Retorna:
    list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    extensiones_set = set(ext.lower() for ext in extensiones)
    archivos_filtrados = [archivo for archivo in archivos if any(archivo.lower().endswith(ext) for ext in extensiones_set)]
    return archivos_filtrados

