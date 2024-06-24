# AnalizadorDeProyecto/tests/test_file_manager.py
import os
import pytest
from unittest.mock import patch, mock_open

from src.file_manager import (
    esta_en_gitignore,
    validar_file_path,
    archivo_permitido,
    leer_contenido_archivo,
    read_and_validate_file,
    procesar_sql,
    copiar_contenido_al_portapapeles,
    verificar_existencia_archivo
)

# Ruta de ejemplo para el proyecto
project_path = "C:\\AppServ\\www\\AnalizadorDeProyecto"

# Mock para el contenido de .gitignore
mock_gitignore_content = "*.pyc\n__pycache__/\n"

# Prueba para verificar si un archivo está en .gitignore
@patch("builtins.open", new_callable=mock_open, read_data=mock_gitignore_content)
def test_esta_en_gitignore(mock_file):
    assert esta_en_gitignore("test.pyc", project_path) is True
    assert esta_en_gitignore("test.py", project_path) is False

# Prueba para validar el tipo de dato del nombre del archivo
def test_validar_file_path():
    assert validar_file_path("test.py") is True
    assert validar_file_path(12345) is False

# Prueba para verificar si un archivo está permitido
def test_archivo_permitido():
    extensiones_permitidas = [".py", ".txt"]
    assert archivo_permitido("test.py", extensiones_permitidas) is True
    assert archivo_permitido("test.exe", extensiones_permitidas) is False

# Prueba para leer el contenido de un archivo
@patch("builtins.open", new_callable=mock_open, read_data="contenido del archivo")
def test_leer_contenido_archivo(mock_file):
    assert leer_contenido_archivo("test.py") == "contenido del archivo"

# Prueba para validar y leer un archivo
@patch("src.file_manager.leer_contenido_archivo", return_value="contenido del archivo")
@patch("os.path.isfile", return_value=True)
@patch("os.path.getsize", return_value=1000)
def test_read_and_validate_file(mock_getsize, mock_isfile, mock_leer_contenido_archivo):
    with patch("src.file_manager.validar_file_path", return_value=True), \
         patch("src.file_manager.archivo_permitido", return_value=True), \
         patch("src.file_manager.esta_en_gitignore", return_value=False):
        assert read_and_validate_file("valid_path", True, [".txt"]) == "contenido del archivo"

    with patch("src.file_manager.validar_file_path", return_value=True), \
         patch("src.file_manager.archivo_permitido", return_value=False):
        assert read_and_validate_file("invalid_extension_path", True, [".txt"]) is None

def test_procesar_sql():
    contenido_sql = "INSERT INTO table_name (col1, col2) VALUES ('val1', 'val2');"
    resultado = procesar_sql(contenido_sql)
    assert "INSERT INTO" in resultado
    assert "VALUES" in resultado

@patch("src.file_manager.pyperclip.copy")
@patch("os.path.exists", return_value=True)
def test_copiar_contenido_al_portapapeles(mock_exists, mock_copy):
    with patch("src.file_manager.read_and_validate_file", return_value="content"):
        copiar_contenido_al_portapapeles("path", [".txt"])
        mock_copy.assert_called_once_with("content")

# Prueba para verificar la existencia de un archivo
@patch("os.path.exists", return_value=True)
def test_verificar_existencia_archivo(mock_exists):
    assert verificar_existencia_archivo("test.py") is True
    mock_exists.assert_called_once_with("test.py")
