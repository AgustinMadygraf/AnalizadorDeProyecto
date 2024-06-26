# tests/test_installer_utils.py
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.installer_utils import verificar_icono

@patch("pathlib.Path.is_file")
def test_verificar_icono(mock_is_file):
    mock_is_file.return_value = True
    assert verificar_icono(Path("fake_path/icon.ico")) == True
    mock_is_file.return_value = False
    assert verificar_icono(Path("fake_path/icon.ico")) == False
