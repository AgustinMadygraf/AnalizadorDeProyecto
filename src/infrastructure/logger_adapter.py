from src.interfaces.logger_port import LoggerPort
from src.logs.config_logger import LoggerConfigurator

class LoggerAdapter(LoggerPort):
    def __init__(self):
        self._logger = LoggerConfigurator().get_logger()

    def debug(self, msg: str):
        self._logger.debug(msg)

    def info(self, msg: str):
        self._logger.info(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def error(self, msg: str):
        self._logger.error(msg)
