from interfaces.logger_port import LoggerPort
from logs.config_logger import LoggerConfigurator

class LoggerAdapter(LoggerPort):
    """
    Adaptador concreto que implementa el puerto LoggerPort.
    Cumple el contrato de Clean Architecture: la infraestructura implementa el puerto,
    la aplicación depende solo de la interfaz.
    """
    def __init__(self):
        self._logger = LoggerConfigurator().get_logger()

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)
