# src/interfaces/logger_event_port.py

from abc import ABC, abstractmethod

class LoggerEventPort(ABC):
    """
    Puerto para eventos de logging desacoplados de la infraestructura.
    La capa de aplicación debe emitir eventos a través de esta interfaz.
    """
    @abstractmethod
    def emit_log(self, level: str, message: str, **kwargs):
        """
        Emitir un evento de log.
        Args:
            level (str): Nivel del log ('info', 'warning', 'error', etc.)
            message (str): Mensaje a registrar
            kwargs: Datos adicionales opcionales
        """
        pass
