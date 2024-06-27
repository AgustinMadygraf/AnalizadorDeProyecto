# tests/test_json_file_manager.py
import pytest
from src.models.json_file_manager import JsonFileManager
from unittest.mock import mock_open, patch
import json

def test_read_file():
    file_manager = JsonFileManager()
    data = {'key': 'value'}
    m = mock_open(read_data=json.dumps(data))
    with patch('builtins.open', m):
        content = file_manager.read_file('test.json')
    assert content == data

def test_process_file():
    file_manager = JsonFileManager()
    data = {'key': 'value'}
    m = mock_open(read_data=json.dumps(data))
    with patch('builtins.open', m):
        content = file_manager.process_file('test.json')
    assert content == json.dumps(data, indent=4)
