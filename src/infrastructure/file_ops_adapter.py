from src.interfaces.file_ops_port import FileOpsPort
from src.file_operations import listar_archivos

class FileOpsAdapter(FileOpsPort):
    def listar_archivos(self, path, extensiones_permitidas):
        return listar_archivos(path, extensiones_permitidas)
