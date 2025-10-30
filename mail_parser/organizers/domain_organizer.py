"""Organize emails by sender domain."""

from pathlib import Path
from typing import Any
import logging
import re

from .base_organizer import BaseOrganizer
from ..core.filename_generator import FilenameGenerator

logger = logging.getLogger(__name__)


class DomainOrganizer(BaseOrganizer):
    """Organize emails by sender's email domain."""

    def __init__(self, base_dir: Path):
        """Initialize with filename generator."""
        super().__init__(base_dir)
        self.filename_gen = FilenameGenerator()

    def get_output_path(self, metadata: dict[str, Any], email_id: str) -> Path:
        """
        Get output path based on sender domain.

        Args:
            metadata: Email metadata
            email_id: Unique email identifier

        Returns:
            Path like: base_dir/by-sender/auricleinc.com/20251028_1444_sender_subject_000123.html
        """
        from_addr = metadata.get('from', {})
        email = from_addr.get('email', '')

        if '@' in email:
            domain = email.split('@')[1].lower()
            # Sanitize domain for filesystem
            domain = self._sanitize_filename(domain)
        else:
            domain = 'unknown'

        # Extract index from email_id
        try:
            email_index = int(email_id.split('_')[-1])
        except (ValueError, IndexError):
            email_index = 0

        # Generate human-readable filename
        filename = self.filename_gen.generate_filename(metadata, email_index)

        path = (
            self.base_dir
            / 'by-sender'
            / domain
            / filename
        )

        self.ensure_directory(path)
        return path

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for filesystem.

        Args:
            filename: Filename to sanitize

        Returns:
            Sanitized filename
        """
        # Replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        # Limit length
        return filename[:255]
