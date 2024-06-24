# AnalizadorDeProeyctos/tests/test_file_operations.py
import os
import pytest
from unittest.mock import patch, mock_open
from src.file_operations import (
    contenido_archivo,
    filtrar_archivos_por_extension,
    asegurar_directorio_docs,
    contar_lineas_codigo,
    listar_archivos
)

# Prueba para concatenar el contenido de archivos
@patch("builtins.open", new_callable=mock_open, read_data="contenido del archivo")
def test_contenido_archivo(mock_file):
    archivos_seleccionados = ["archivo1.txt", "archivo2.txt"]
    resultado = contenido_archivo(archivos_seleccionados)
    assert "contenido del archivo" in resultado

# Prueba para filtrar archivos por extensión
def test_filtrar_archivos_por_extension():
    archivos = ["archivo1.py", "archivo2.txt", "archivo3.md"]
    extensiones = [".py", ".txt"]
    resultado = filtrar_archivos_por_extension(archivos, extensiones)
    assert len(resultado) == 2
    assert "archivo1.py" in resultado
    assert "archivo2.txt" in resultado

# Prueba para asegurar que el directorio docs existe
@patch("os.path.exists", return_value=False)
@patch("os.makedirs")
def test_asegurar_directorio_docs(mock_makedirs, mock_exists):
    ruta = "test_path"
    asegurar_directorio_docs(ruta)
    mock_makedirs.assert_called_once_with(os.path.join(ruta, 'docs'))

# Prueba para contar líneas de código en un archivo
@patch("builtins.open", new_callable=mock_open, read_data="# comentario\nlinea de codigo\n\n")
def test_contar_lineas_codigo(mock_file):
    extensiones_codigo = {".py", ".ino", ".h"}
    resultado = contar_lineas_codigo("archivo.py", extensiones_codigo)
    assert resultado == 1

# Prueba para listar archivos y su estructura
@patch("os.walk")
@patch("os.path.getsize", return_value=1024)
@patch("src.file_operations.contar_lineas_codigo", return_value=10)
def test_listar_archivos(mock_contar_lineas, mock_getsize, mock_walk):
    mock_walk.return_value = [
        ("root", ("dir1",), ("file1.py", "file2.txt")),
        ("root/dir1", (), ("file3.md", "file4.py")),
    ]
    archivos, estructura = listar_archivos("root", [".py", ".txt", ".md"])
    assert len(archivos) == 4
    assert "root/" in estructura[0]
    assert "file1.py" in estructura[1]
