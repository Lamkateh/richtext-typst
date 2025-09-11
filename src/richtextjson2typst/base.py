from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Common interface for all rich text JSON parsers."""

    @abstractmethod
    def parse(self, data: dict) -> str:
        """Convert a given JSON to Typst string."""
        pass
