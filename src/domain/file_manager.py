# Dominio: Entidad principal para gestión de archivos
# ...mover aquí la lógica de negocio pura relacionada a archivos...

class FileManager:
    def __init__(self, project_path, handler_port):
        self.project_path = project_path
        self.gitignore_patterns = self._leer_gitignore()
        self.handler_port = handler_port  # Puerto abstracto para handlers

    def _leer_gitignore(self):
        # ...lógica igual...
        # (No depende de infraestructura externa)
        return []  # Asegurar retorno explícito

    def esta_en_gitignore(self, ruta_archivo):
        # ...existing code...
        pass

    def read_file(self, file_path):
        return self.handler_port.read_file(file_path)

    def process_file(self, file_path):
        return self.handler_port.process_file(file_path)

    def validar_file_path(self, file_path):
        # ...existing code...
        pass

    def read_and_validate_file(self, file_path, permitir_lectura, extensiones_permitidas, validaciones_extras=None):
        if validaciones_extras is None:
            validaciones_extras = []
        # ...existing code...
        pass

    def es_archivo_valido(self, file_path, extensiones_permitidas, permitir_lectura, validaciones_extras):
        # ...existing code...
        pass

    def archivo_permitido(self, file_path, extensiones_permitidas):
        # ...existing code...
        pass

    def es_acceso_permitido(self, file_path, validaciones_extras):
        # ...existing code...
        pass
