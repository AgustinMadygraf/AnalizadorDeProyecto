# src/utilities.py
"""
Módulo transversal de utilidades generales.

- Solo debe contener funciones puramente utilitarias (sin lógica de dominio ni dependencias a infraestructura).
- Si una función depende de infraestructura, muévala a src/infrastructure/.
- Si una función es específica de una capa, ubíquela en la capa correspondiente.
"""

import sys
import os
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()

def obtener_version_python():
    return sys.version

def limpieza_pantalla():
    print("\033[H\033[J", end="")
    logger.debug("Pantalla limpiada.")

