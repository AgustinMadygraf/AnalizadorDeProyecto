#SCR/SalidDatos.py
import os
import time
from GestArch import leer_archivo, copiar_contenido_al_portapapeles
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def generar_archivo_salida(ruta, modo_prompt, extensiones, ruta_proyecto):
    """
    Genera el archivo de salida con la estructura dada.

    Args:
        ruta (str): Ruta del directorio donde se generará el archivo de salida.
        estructura (list): Estructura de directorios y archivos a incluir en el archivo de salida.
        modo_prompt (str): Modo seleccionado para la salida.
        extensiones (list of str): Extensiones para filtrar archivos.
        ruta_proyecto (str): Ruta base del proyecto.
    """
    asegurar_directorio_AMIS(ruta_proyecto)
    archivos_encontrados, estructura_actualizada = listar_archivos(ruta, extensiones)
    nombre_archivo_salida = generar_nombre_archivo_salida(ruta)
    formatear_archivo_salida(nombre_archivo_salida)
    contenido = preparar_contenido_salida(estructura_actualizada, modo_prompt, archivos_encontrados, ruta_proyecto)
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
        logger.debug(f"El contenido de {nombre_archivo_salida} ha sido eliminado.")
    except Exception as e:
        logger.warning(f"Error al intentar formatear el archivo {nombre_archivo_salida}: {e}")

def preparar_contenido_salida(estructura, modo_prompt, archivos_seleccionados, ruta_proyecto):
    """
    Prepara el contenido de salida para un archivo Markdown.

    Esta función genera una sección de Markdown que incluye tanto la estructura
    de carpetas y archivos del proyecto como el contenido de archivos seleccionados.
    Cada sección se formatea adecuadamente para una visualización clara en Markdown.

    Args:
        estructura (list): Lista que representa la estructura de carpetas y archivos.
        modo_prompt (str): Nombre del archivo que contiene el prompt inicial o plantilla.
        archivos_seleccionados (list): Lista de rutas de archivos cuyo contenido se incluirá.

    Returns:
        str: El contenido completo formateado para Markdown.
    """

    logger.debug("Preparando contenido de salida")
    nombre_archivo = os.path.join(ruta_proyecto, modo_prompt)
    contenido_prompt = leer_archivo(nombre_archivo)
    contenido_prompt = leer_archivo(nombre_archivo)

    # Comprobación y asignación del contenido inicial basado en el prompt.
    contenido = contenido_prompt if contenido_prompt else "\n\nprompt:\nNo hay prompt. falla.\n\n"

    # Añadiendo la estructura de directorios y archivos en formato Markdown.
    contenido += "\n\n## Estructura de Carpetas y Archivos\n```bash\n"
    contenido += '\n'.join(estructura) + "\n```\n"

    # Procesamiento y adición de contenido de archivos seleccionados.
    if archivos_seleccionados:
        contenido += "\n\n## Contenido de Archivos Seleccionados\n"
        for archivo in archivos_seleccionados:
            contenido_archivo = leer_archivo(archivo)
            if contenido_archivo:
                # Formatear el contenido del archivo para Markdown.
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
    # Lista de caracteres que pueden interferir con el formato Markdown.
    caracteres_a_escapar = ['*', '_', '`', '!', '[', ']', '(', ')']
    for char in caracteres_a_escapar:
        texto = texto.replace(char, f'\\{char}')
    return texto

def generar_nombre_archivo_salida(ruta):
    """
    Genera el nombre del archivo de salida basado en la ruta y un nombre base.

    Args:
        ruta (str): Ruta del directorio para el archivo de salida.
        nombre_base (str): Nombre base para el archivo de salida.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    # Formatear la ruta para el nombre del archivo
    nombre_archivo_salida = f"AMIS\\00-Prompt-for-ProjectAnalysis.md" #AMIS = Analysis and Modification Improvement System
    return os.path.join(ruta, nombre_archivo_salida)

def escribir_archivo_salida(nombre_archivo, contenido):
    """
    Escribe el contenido dado en el archivo de salida especificado y maneja los errores de manera más detallada.

    Args:
        nombre_archivo (str): Ruta del archivo donde se escribirá el contenido.
        contenido (str): Contenido a escribir en el archivo.
    """
    if contenido is None:
        logger.error(f"Se intentó escribir contenido 'None' en el archivo {nombre_archivo}.")
        return False

    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        logger.info(f"Archivo de salida generado exitosamente: {nombre_archivo}")
        return True
    except IOError as e:
        logger.error(f"Error de E/S al escribir en el archivo {nombre_archivo}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al escribir en el archivo {nombre_archivo}: {e}")
    
    return False

def contenido_archivo(archivos_seleccionados):
    """
    Concatena el contenido de una lista de archivos seleccionados en un solo string.

    Esta función itera sobre una lista de rutas de archivos, leyendo y agregando el contenido de cada uno a una cadena.
    En caso de un error durante la lectura de un archivo (por ejemplo, si el archivo no existe o no es accesible),
    se agrega un mensaje de error específico a la cadena resultante.

    Args:
        archivos_seleccionados (list of str): Una lista de rutas de archivos cuyos contenidos se desean concatenar.

    Returns:
        str: Una cadena que contiene el contenido concatenado de todos los archivos seleccionados, 
             con cada contenido de archivo precedido por un encabezado que indica el nombre del archivo,
             y seguido de cualquier mensaje de error que ocurra durante la lectura de los archivos.

    Nota:
        Esta función está diseñada para manejar texto. No es adecuada para archivos binarios.
    """
    contenido_total = ""

    # Itera a través de cada archivo en la lista de archivos seleccionados
    for archivo in archivos_seleccionados:
        try:
            # Intenta leer el contenido del archivo
            with open(archivo, 'r', encoding='utf-8') as file:
                contenido = file.read()
                # Añade un encabezado y el contenido del archivo a la cadena total
                contenido_total += f"\n--- Contenido de {archivo} ---\n"
                contenido_total += contenido + "\n"
        except Exception as e:
            # En caso de error, añade un mensaje de error a la cadena total
            contenido_total += f"\nError al leer el archivo {archivo}: {e}\n"

    return contenido_total
    
def listar_archivos(ruta, extensiones):
    """
    Genera una lista de archivos y su estructura de directorio basada en una ruta y extensiones específicas.

    Esta función recorre recursivamente todos los directorios y subdirectorios a partir de una ruta dada,
    filtrando los archivos según las extensiones proporcionadas. Ignora explícitamente los directorios '.git'.
    Genera dos listas: una con las rutas completas de los archivos filtrados y otra con la estructura
    de directorios y archivos representada en forma de texto para su presentación.

    Args:
        ruta (str): La ruta del directorio raíz desde donde iniciar el escaneo de archivos.
        extensiones (list of str): Una lista de extensiones de archivo para filtrar los archivos.

    Returns:
        tuple: 
            - Una lista de rutas completas de archivos que cumplen con las extensiones dadas.
            - Una lista de cadenas que representa la estructura de directorios y archivos.
            
    Raises:
        Exception: Proporciona información sobre cualquier error que ocurra durante la ejecución de la función.
    """
    try:
        archivos_encontrados = []
        estructura = []

        for raiz, _, archivos in os.walk(ruta):
            # Ignora los directorios .git
            if '.git' in raiz:
                continue

            # Calcula el nivel de indentación basado en la profundidad del directorio.
            nivel = raiz.replace(ruta, '').count(os.sep)
            indentacion = ' ' * 4 * nivel
            estructura.append(f"{indentacion}{os.path.basename(raiz)}/")

            # Aplica una subindentación para los archivos dentro de cada directorio.
            subindentacion = ' ' * 4 * (nivel + 1)

            # Filtra y procesa los archivos en el directorio actual.
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

def asegurar_directorio_AMIS(ruta):
    """
    Asegura que exista el directorio AMIS en la ruta dada.
    Si el directorio no existe, lo crea.

    Args:
        ruta (str): Ruta base donde se debe encontrar o crear el directorio AMIS.
    """
    directorio_amis = os.path.join(ruta, 'AMIS')
    if not os.path.exists(directorio_amis):
        os.makedirs(directorio_amis)
        logger.info(f"Directorio AMIS creado en {directorio_amis}")
    else:
        logger.debug(f"Directorio AMIS ya existe en {directorio_amis}")
