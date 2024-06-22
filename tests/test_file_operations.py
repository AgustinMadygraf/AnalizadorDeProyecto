import pytest
from src.file_operations import contenido_archivo, filtrar_archivos_por_extension, contar_lineas_codigo

def test_contenido_archivo(tmpdir):
    file1 = tmpdir.join("file1.txt")
    file2 = tmpdir.join("file2.txt")
    file1.write("contenido de prueba 1")
    file2.write("contenido de prueba 2")
    assert "contenido de prueba 1" in contenido_archivo([str(file1), str(file2)])
    assert "contenido de prueba 2" in contenido_archivo([str(file1), str(file2)])
    assert "Error" not in contenido_archivo([str(file1), str(file2)])

def test_filtrar_archivos_por_extension(tmpdir):
    file1 = tmpdir.join("file1.txt")
    file2 = tmpdir.join("file2.md")
    file3 = tmpdir.join("file3.py")
    files = [str(file1), str(file2), str(file3)]
    assert len(filtrar_archivos_por_extension(files, [".txt"])) == 1
    assert len(filtrar_archivos_por_extension(files, [".md", ".py"])) == 2

def test_contar_lineas_codigo(tmpdir):
    file = tmpdir.join("file.py")
    file.write("linea 1\n#linea de comentario\n\nlinea 2")
    assert contar_lineas_codigo(str(file), {".py"}) == 2
    assert contar_lineas_codigo(str(file), {".txt"}) == None
