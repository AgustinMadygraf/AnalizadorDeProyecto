# src/presentation/i18n/__init__.py
"""
Carga el diccionario de idioma según variable de entorno o parámetro.
Provee LANG como dict global para la UI.
"""

import os
import json

IDIOMAS = {
    'es': 'es.json',
    'en': 'en.json',
}

lang_code = os.environ.get('ANALIZADOR_LANG', 'es')
lang_file = os.path.join(os.path.dirname(__file__), IDIOMAS.get(lang_code, 'es.json'))
try:
    with open(lang_file, 'r', encoding='utf-8') as f:
        LANG = json.load(f)
except Exception:
    LANG = {}
