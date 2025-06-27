# tests/test_file_manager.py
import pytest
from unittest.mock import Mock
from src.interfaces.i_file_manager import IFileManager

class FakeFileManager(IFileManager):
    def read_file(self, file_path):
        if file_path == "valid_path":
            return "contenido"
        raise FileNotFoundError
    def process_file(self, file_path):
        return f"procesado:{file_path}"

def test_read_file():
    fm = FakeFileManager()
    assert fm.read_file("valid_path") == "contenido"
    with pytest.raises(FileNotFoundError):
        fm.read_file("invalid_path")

def test_process_file():
    fm = FakeFileManager()
    assert fm.process_file("algo.txt") == "procesado:algo.txt"
