from src.interfaces.event_handler_port import IEventHandlerPort

class EventHandlerAdapter(IEventHandlerPort):
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
