import os
import logging

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
