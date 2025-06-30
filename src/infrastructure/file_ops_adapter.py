from src.interfaces.file_ops_port import FileOpsPort
from src.infrastructure.file_operations_adapter import listar_archivos
from src.infrastructure.file_operations_adapter import contar_lineas_codigo

# TODO: Revisar posible código muerto (vulture): clase 'FileOpsAdapter' reportada como sin uso
class FileOpsAdapter(FileOpsPort):
    """
    Adaptador concreto que implementa el puerto FileOpsPort.
    Cumple Clean Architecture: la infraestructura implementa el puerto,
    la aplicación depende solo de la interfaz.
    """
    def __init__(self, logger_port):
        self.logger = logger_port

    def listar_archivos(self, path, extensiones_permitidas):
        return listar_archivos(path, extensiones_permitidas, self.logger)
    
    def contar_lineas_codigo(self, file_path, extensiones_codigo):
        return contar_lineas_codigo(file_path, extensiones_codigo, self.logger)
