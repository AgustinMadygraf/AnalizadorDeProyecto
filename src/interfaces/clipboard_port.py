from abc import ABC, abstractmethod

class ClipboardPort(ABC):
    """Contract for clipboard operations."""
    @abstractmethod
    def copy(self, data: str) -> None:
        """Copy data to clipboard."""
        pass

    @abstractmethod
    def paste(self) -> str:
        """Paste data from clipboard."""
        pass
