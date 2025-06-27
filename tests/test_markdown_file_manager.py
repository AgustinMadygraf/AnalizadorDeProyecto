# tests/test_markdown_file_manager.py
import pytest
from src.domain.markdown_file_manager import MarkdownFileManager
from unittest.mock import mock_open, patch

def test_read_file():
    file_manager = MarkdownFileManager()
    m = mock_open(read_data="# Header")
    with patch('builtins.open', m):
        content = file_manager.read_file('test.md')
    assert content == "# Header"

def test_process_file():
    file_manager = MarkdownFileManager()
    m = mock_open(read_data="# Header")
    with patch('builtins.open', m):
        content = file_manager.process_file('test.md')
    assert content == "# Header"
