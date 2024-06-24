# AnalizadorDeProeyctos/src/test_file_operations.py
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
        ("root", ["dir"], ["archivo1.py", "archivo2.txt"])
    ]
    extensiones_permitidas = [".py", ".txt"]
    archivos_encontrados, estructura = listar_archivos("root", extensiones_permitidas)
    assert len(archivos_encontrados) == 2
    assert "archivo1.py" in archivos_encontrados
    assert "archivo2.txt" in archivos_encontrados
    assert any("archivo1.py" in s for s in estructura)
    assert any("archivo2.txt" in s for s in estructura)
