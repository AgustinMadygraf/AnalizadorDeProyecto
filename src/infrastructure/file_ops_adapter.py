from src.interfaces.file_ops_port import FileOpsPort
from src.infrastructure.file_operations_adapter import listar_archivos
from src.infrastructure.file_operations_adapter import contar_lineas_codigo

class FileOpsAdapter(FileOpsPort):
    def __init__(self, logger_port):
        self.logger = logger_port

    def listar_archivos(self, path, extensiones_permitidas):
        return listar_archivos(path, extensiones_permitidas)
    
    def contar_lineas_codigo(self, file_path, extensiones_codigo):
        return contar_lineas_codigo(file_path, extensiones_codigo, self.logger)
