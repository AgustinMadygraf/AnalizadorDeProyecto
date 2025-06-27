# src/infrastructure/utils/screen_utils.py
from src.logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

def limpieza_pantalla():
    print("\033[H\033[J", end="")
    logger.debug("Pantalla limpiada.")
