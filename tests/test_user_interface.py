import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from domain.user_interface import UserInterface
from unittest.mock import MagicMock, patch

# Dummy logger para inyectar en UserInterface
class DummyLogger:
    def debug(self, *a, **kw): pass
    def info(self, *a, **kw): pass
    def warning(self, *a, **kw): pass
    def error(self, *a, **kw): pass


def test_solicitar_opcion_valida():
    ui = UserInterface(DummyLogger())
    mensaje = "Seleccione una opción:"
    opciones = {1: 'opcion1', 2: 'opcion2'}
    
    with patch('builtins.input', side_effect=['1']):
        resultado = ui.solicitar_opcion(mensaje, opciones)
        assert resultado == 'opcion1'

def test_solicitar_opcion_invalida():
    ui = UserInterface(DummyLogger())
    mensaje = "Seleccione una opción:"
    opciones = {1: 'opcion1', 2: 'opcion2'}
    
    with patch('builtins.input', side_effect=['3', '2']):
        resultado = ui.solicitar_opcion(mensaje, opciones)
        assert resultado == 'opcion2'

def test_menu_0():
    ui = UserInterface(DummyLogger())
    
    with patch('builtins.input', side_effect=['/ruta/de/prueba']):
        resultado = ui.menu_0()
        assert resultado == '/ruta/de/prueba'

def test_menu_1():
    ui = UserInterface(DummyLogger())
    
    with patch('builtins.input', side_effect=['1']):
        resultado = ui.menu_1()
        assert resultado == 'config\\prompt_1.md'
