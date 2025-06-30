# pylint: disable=import-error
from src.interfaces.logger_port import LoggerPort
from src.interfaces.logger_event_port import LoggerEventPort
from src.logs.config_logger import LoggerConfigurator

class LoggerAdapter(LoggerPort, LoggerEventPort):
    """
    Adaptador concreto que implementa los puertos LoggerPort y LoggerEventPort.
    Cumple el contrato de Clean Architecture: la infraestructura implementa los puertos,
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

    def emit_log(self, level: str, message: str, **kwargs):
        """
        Implementación de LoggerEventPort: permite logging desacoplado por nivel.
        """
        log_method = getattr(self._logger, level.lower(), None)
        if callable(log_method):
            log_method(message, **kwargs)
        else:
            self._logger.info(f"[LoggerEventPort] {level.upper()}: {message}", **kwargs)
