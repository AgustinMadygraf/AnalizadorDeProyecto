import os
import datetime
from interfaces.file_manager_port import FileManagerPort
from interfaces.file_ops_port import FileOpsPort
from interfaces.content_manager_port import ContentManagerPort
from interfaces.clipboard_port import ClipboardPort
from interfaces.logger_port import LoggerPort
# Dominio: Entidad para generación de reportes
# ...mover aquí la lógica de negocio pura relacionada a reportes...

class ReportGenerator:
    def __init__(
        self,
        project_path: str,
        file_manager_port: FileManagerPort,
        file_ops_port: FileOpsPort,
        content_manager_port: ContentManagerPort,
        clipboard_port: ClipboardPort,
        event_handler=None,  # Puede ser None o un adaptador con publish
    ):
        self.project_path = project_path
        self.file_manager = file_manager_port
        self.file_ops = file_ops_port
        self.content_manager = content_manager_port
        self.clipboard = clipboard_port
        self.event_handler = event_handler

    def _emit_event(self, level, message):
        if self.event_handler and hasattr(self.event_handler, 'publish'):
            self.event_handler.publish('log', {'level': level, 'message': message})

    def generar_archivo_salida(self, path, modo_prompt, extensiones_permitidas, ruta_archivos, incluir_todo):
        self.content_manager.asegurar_directorio_docs(path)
        archivos_encontrados, estructura_actualizada = self.file_ops.listar_archivos(path, extensiones_permitidas)
        nombre_archivo_salida = self.generar_nombre_archivo_salida(path)
        self.formatear_archivo_salida(nombre_archivo_salida)
        contenido = self.preparar_contenido_salida(estructura_actualizada, modo_prompt, archivos_encontrados, path, ruta_archivos, extensiones_permitidas)
        self.escribir_archivo_salida(nombre_archivo_salida, contenido)
        self.clipboard.copiar_contenido_al_portapapeles(nombre_archivo_salida, extensiones_permitidas)
        print("")
        return nombre_archivo_salida

    def formatear_archivo_salida(self, nombre_archivo_salida):
        try:
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
                archivo.write('')
            self._emit_event('debug', f"El contenido de {nombre_archivo_salida} ha sido eliminado.")
        except Exception as e:
            self._emit_event('warning', f"Error al intentar formatear el archivo {nombre_archivo_salida}: {e}")

    def preparar_contenido_salida(self, estructura, modo_prompt, archivos_seleccionados, path, ruta_archivo, extensiones_permitidas):
        self._emit_event('debug', "Preparando contenido de salida")
        contenido_prompt = self.file_manager.read_and_validate_file(os.path.join(ruta_archivo, modo_prompt), permitir_lectura=True, extensiones_permitidas=extensiones_permitidas) or "\n\nPrompt:\nNo hay prompt. Falla.\n\n"
        contenido = contenido_prompt
        ruta_todo_txt = os.path.join(path, 'todo.txt')
        if os.path.exists(ruta_todo_txt):
            with open(ruta_todo_txt, 'r', encoding='utf-8') as todo_file:
                contenido_todo_txt = todo_file.read()
                contenido += "\n## TODO List from todo.txt\n" + contenido_todo_txt + "\n"
        contenido += "\n\n## Estructura de Carpetas y Archivos\n```bash\n" + '\n'.join(estructura) + "\n```\n"
        if archivos_seleccionados:
            contenido += self.construir_contenido_archivos_seleccionados(archivos_seleccionados, extensiones_permitidas)
        else:
            self._emit_event('warning', "No se han proporcionado archivos seleccionados para incluir en el contenido")
        contenido += "Fecha y hora:\n"
        contenido += datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n\n"
        return contenido

    def construir_contenido_archivos_seleccionados(self, archivos_seleccionados, extensiones_permitidas):
        contenido_archivos = "\n\n## Contenido de Archivos Seleccionados\n"
        for archivo in archivos_seleccionados:
            contenido_archivo = self.file_manager.process_file(archivo)
            if contenido_archivo:
                extension = os.path.splitext(archivo)[1]
                if extension == ".json":
                    contenido_archivos += f"\n### {archivo}\n```json\n{contenido_archivo}\n```\n"
                else:
                    contenido_archivos += f"\n### {archivo}\n```plaintext\n{contenido_archivo}\n```\n"
            else:
                self._emit_event('debug', f"No se pudo obtener el contenido del archivo: {archivo}")
        return contenido_archivos

    def generar_nombre_archivo_salida(self, path):
        nombre_archivo_salida = f"docs\\00-Prompt-for-ProjectAnalysis.md"
        return os.path.join(path, nombre_archivo_salida)

    def escribir_archivo_salida(self, nombre_archivo, contenido):
        if contenido is None:
            self._emit_event('error', f"Se intentó escribir contenido 'None' en el archivo {nombre_archivo}.")
            return False
        self._emit_event('debug', f"Intentando escribir en el archivo: {nombre_archivo}")
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            self._emit_event('info', "Archivo de salida generado exitosamente:")
            self._emit_event('info', nombre_archivo)
            return True
        except IOError as e:
            self._emit_event('error', f"Error de E/S al escribir en el archivo {nombre_archivo}: {e}")
        except Exception as e:
            self._emit_event('error', f"Error inesperado al escribir en el archivo {nombre_archivo}: {e}")
        return False

    def generar_archivo_salida_rapido(self, path, extensiones_permitidas):
        """
        Genera un archivo de salida rápido con solo la estructura de carpetas y archivos.
        """
        self.content_manager.asegurar_directorio_docs(path)
        archivos_encontrados, estructura_actualizada = self.file_ops.listar_archivos(path, extensiones_permitidas)
        nombre_archivo_salida = self.generar_nombre_archivo_salida(path)
        self.formatear_archivo_salida(nombre_archivo_salida)
        contenido = "## Estructura de Carpetas y Archivos\n```bash\n" + '\n'.join(estructura_actualizada) + "\n```\n"
        self.escribir_archivo_salida(nombre_archivo_salida, contenido)
        self.clipboard.copiar_contenido_al_portapapeles(nombre_archivo_salida, extensiones_permitidas)
        print("")
        return nombre_archivo_salida
