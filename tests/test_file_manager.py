# tests/test_file_manager.py
import pytest
import os
from src.models.file_manager import FileManager
from unittest.mock import patch, mock_open

@pytest.fixture
def file_manager():
    return FileManager("C:\\AppServ\\www\\AnalizadorDeProyecto")

def test_leer_gitignore(file_manager, mocker):
    mocker.patch("builtins.open", mock_open(read_data="*.pyc\n__pycache__\n"))
    patrones = file_manager._leer_gitignore()
    assert "*.pyc" in patrones
    assert "__pycache__" in patrones

def test_validar_file_path(file_manager):
    assert file_manager.validar_file_path("valid_path")
    assert not file_manager.validar_file_path(123)

def test_archivo_permitido(file_manager):
    extensiones_permitidas = ['.txt', '.md']
    assert file_manager.archivo_permitido("file.txt", extensiones_permitidas)
    assert not file_manager.archivo_permitido("file.exe", extensiones_permitidas)
