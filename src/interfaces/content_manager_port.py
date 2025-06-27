from abc import ABC, abstractmethod

class ContentManagerPort(ABC):
    """Contract for content management operations."""
    @abstractmethod
    def load_content(self, source: str) -> str:
        """Load content from a source (file, db, etc)."""
        pass

    @abstractmethod
    def save_content(self, destination: str, content: str) -> None:
        """Save content to a destination (file, db, etc)."""
        pass
