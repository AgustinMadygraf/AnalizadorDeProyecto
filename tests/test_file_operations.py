# tests/test_file_operations.py
import pytest
from src.interfaces.file_ops_port import FileOpsPort

class FakeFileOps(FileOpsPort):
    def listar_archivos(self, path, extensiones_permitidas):
        # Simula estructura de archivos
        return [f"{path}/archivo1.py", f"{path}/archivo2.txt"], ["estructura1", "estructura2"]
    def contar_lineas_codigo(self, file_path, extensiones_codigo):
        return 42

def test_listar_archivos():
    fake_ops = FakeFileOps()
    archivos, estructura = fake_ops.listar_archivos('/ruta', {'.py', '.txt'})
    assert len(archivos) == 2
    assert archivos[0].endswith('archivo1.py')
    assert archivos[1].endswith('archivo2.txt')
    assert len(estructura) == 2

def test_contar_lineas_codigo():
    fake_ops = FakeFileOps()
    assert fake_ops.contar_lineas_codigo('algo.py', {'.py'}) == 42
