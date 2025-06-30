from src.interfaces.event_handler_port import IEventHandlerPort

# TODO: Revisar posible código muerto (vulture): clase 'EventHandlerAdapter' y método 'subscribe' reportados como sin uso
class EventHandlerAdapter(IEventHandlerPort):
    """
    Adaptador concreto que implementa el puerto IEventHandlerPort.
    Cumple Clean Architecture: la infraestructura implementa el puerto,
    la aplicación depende solo de la interfaz.
    """
    def __init__(self, logger_port):
        self.logger = logger_port
        self._subscribers = {}

    def publish(self, event: str, payload: dict) -> None:
        self.logger.info(f"Evento publicado: {event} | Payload: {payload}")
        handlers = self._subscribers.get(event, [])
        for handler in handlers:
            handler(payload)

    def subscribe(self, event: str, handler) -> None:
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(handler)
