import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from domain.markdown_file_manager import MarkdownFileManager
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
