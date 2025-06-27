from abc import ABC, abstractmethod

class IEventHandlerPort(ABC):
    @abstractmethod
    def publish(self, event: str, payload: dict) -> None:
        pass

    @abstractmethod
    def subscribe(self, event: str, handler) -> None:
        pass
