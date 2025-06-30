# src/presentation/i18n/__init__.py
"""
Carga el diccionario de idioma según variable de entorno o parámetro.
Provee LANG como dict global para la UI.
"""

import os
import json
import warnings

IDIOMAS = {
    'es': 'es.json',
    'en': 'en.json',
}

def cargar_idioma(lang_code):
    lang_file = os.path.join(os.path.dirname(__file__), IDIOMAS.get(lang_code, 'es.json'))
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        warnings.warn(f"[WARN] No se pudo cargar el archivo de idioma '{lang_code}': {e}. Usando español por defecto.")
        if lang_code != 'es':
            try:
                with open(os.path.join(os.path.dirname(__file__), 'es.json'), 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e2:
                warnings.warn(f"[ERROR] No se pudo cargar el idioma por defecto: {e2}. Se usará mensajes internos.")
        return {}

lang_code = os.environ.get('ANALIZADOR_LANG', 'es')
LANG = cargar_idioma(lang_code)
