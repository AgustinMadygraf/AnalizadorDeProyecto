from src.interfaces.file_ops_port import FileOpsPort
from src.infrastructure.file_operations_adapter import listar_archivos
from src.infrastructure.file_operations_adapter import contar_lineas_codigo
from src.infrastructure.logger_adapter import LoggerAdapter

class FileOpsAdapter(FileOpsPort):
    def listar_archivos(self, path, extensiones_permitidas):
        return listar_archivos(path, extensiones_permitidas)
    
    def contar_lineas_codigo(self, file_path, extensiones_codigo):
        logger = LoggerAdapter()
        return contar_lineas_codigo(file_path, extensiones_codigo, logger)
