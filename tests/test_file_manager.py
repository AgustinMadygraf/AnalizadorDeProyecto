#AnalizadorDeProyectos/test/test_file_manager.py
import pytest
from src.file_manager import validar_file_path, archivo_permitido, leer_contenido_archivo, read_and_validate_file

def test_validar_file_path():
    assert validar_file_path("test.txt") == True
    assert validar_file_path(123) == False

def test_archivo_permitido():
    assert archivo_permitido("Pipfile", [".txt", ".md"]) == True
    assert archivo_permitido("test.txt", [".txt", ".md"]) == True
    assert archivo_permitido("test.exe", [".txt", ".md"]) == False

def test_leer_contenido_archivo(tmpdir):
    file = tmpdir.join("test.txt")
    file.write("contenido de prueba")
    assert leer_contenido_archivo(str(file)) == "contenido de prueba"
    assert leer_contenido_archivo("no_existe.txt") == None

def test_read_and_validate_file(tmpdir):
    file = tmpdir.join("test.txt")
    file.write("contenido de prueba")
    assert read_and_validate_file(str(file), True, [".txt", ".md"]) == "contenido de prueba"
    assert read_and_validate_file("no_existe.txt", True, [".txt", ".md"]) == None
