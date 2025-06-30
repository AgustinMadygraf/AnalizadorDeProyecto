import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from unittest.mock import Mock
from src.domain.file_manager import FileManager

class DummyHandler:
    def read_file(self, file_path):
        return f"read:{file_path}"
    def process_file(self, file_path):
        return f"process:{file_path}"

class DummyFactory:
    def get_handler(self, extension):
        if extension == ".dummy":
            return DummyHandler()
        return None

def test_file_manager_uses_factory_for_read():
    fm = FileManager(project_path="/tmp", logger_port=Mock(), handler_factory=DummyFactory())
    result = fm.read_file("archivo.dummy")
    assert result == "read:archivo.dummy"

def test_file_manager_uses_factory_for_process():
    fm = FileManager(project_path="/tmp", logger_port=Mock(), handler_factory=DummyFactory())
    result = fm.process_file("archivo.dummy")
    assert result == "process:archivo.dummy"

def test_file_manager_returns_none_for_unknown_extension():
    fm = FileManager(project_path="/tmp", logger_port=Mock(), handler_factory=DummyFactory())
    result = fm.read_file("archivo.unknown")
    assert result is None
