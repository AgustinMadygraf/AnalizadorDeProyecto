from abc import ABC, abstractmethod

class LoggerPort(ABC):
    @abstractmethod
    def debug(self, msg: str):
        pass

    @abstractmethod
    def info(self, msg: str):
        pass

    @abstractmethod
    def warning(self, msg: str):
        pass

    @abstractmethod
    def error(self, msg: str):
        pass
