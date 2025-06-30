from abc import ABC, abstractmethod

class IEventHandlerPort(ABC):
    @abstractmethod
    def publish(self, event: str, payload: dict) -> None:
        pass

    @abstractmethod
    # TODO: Revisar posible código muerto (vulture): método 'subscribe' reportado como sin uso
    def subscribe(self, event: str, handler) -> None:
        pass
