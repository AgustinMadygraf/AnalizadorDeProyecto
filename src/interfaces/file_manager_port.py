from abc import ABC, abstractmethod

class FileManagerPort(ABC):
    """Contract for file management operations."""
    @abstractmethod
    def read(self, path: str) -> str:
        """Read file content from path."""
        pass

    @abstractmethod
    def write(self, path: str, content: str) -> None:
        """Write content to file at path."""
        pass
