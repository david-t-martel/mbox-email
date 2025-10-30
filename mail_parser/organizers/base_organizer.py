"""Base organizer class."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseOrganizer(ABC):
    """Base class for email organizers."""

    def __init__(self, base_dir: Path):
        """
        Initialize organizer.

        Args:
            base_dir: Base output directory
        """
        self.base_dir = Path(base_dir)

    @abstractmethod
    def get_output_path(self, metadata: dict[str, Any], email_id: str) -> Path:
        """
        Get output path for an email.

        Args:
            metadata: Email metadata
            email_id: Unique email identifier

        Returns:
            Output path for the email
        """
        pass

    def ensure_directory(self, path: Path) -> None:
        """
        Ensure directory exists.

        Args:
            path: Directory path
        """
        path.parent.mkdir(parents=True, exist_ok=True)
