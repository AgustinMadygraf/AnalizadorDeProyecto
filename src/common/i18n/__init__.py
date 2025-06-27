# src/common/i18n/__init__.py
import os
import json

LANG_ENV = os.environ.get('ANALIZADOR_LANG', 'es')
LANG_FILE = os.path.join(os.path.dirname(__file__), f'{LANG_ENV}.json')

def load_lang():
    try:
        with open(LANG_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Fallback a español si hay error
        with open(os.path.join(os.path.dirname(__file__), 'es.json'), encoding='utf-8') as f:
            return json.load(f)

LANG = load_lang()
