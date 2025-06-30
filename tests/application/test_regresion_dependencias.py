"""
Test de regresión: la capa de aplicación no debe depender de adaptadores concretos de infraestructura.
Falla si se detecta una importación directa desde src/infrastructure/ en src/application/.
"""
import ast
import os
import sys

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/application'))
INFRA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/infrastructure'))


def find_infra_imports(pyfile):
    with open(pyfile, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=pyfile)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and 'infrastructure' in node.module:
                return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'infrastructure' in alias.name:
                    return True
    return False

def test_no_infra_imports_in_application():
    for root, _, files in os.walk(APP_PATH):
        for file in files:
            if file.endswith('.py'):
                pyfile = os.path.join(root, file)
                assert not find_infra_imports(pyfile), f"Importación de infraestructura detectada en {pyfile}"
