"""Organize emails by date."""

from pathlib import Path
from typing import Any
from datetime import datetime
import logging

from .base_organizer import BaseOrganizer
from ..core.filename_generator import FilenameGenerator

logger = logging.getLogger(__name__)


class DateOrganizer(BaseOrganizer):
    """Organize emails by date (year/month/day structure)."""

    def __init__(self, base_dir: Path):
        """Initialize with filename generator."""
        super().__init__(base_dir)
        self.filename_gen = FilenameGenerator()

    def get_output_path(self, metadata: dict[str, Any], email_id: str) -> Path:
        """
        Get output path based on email date.

        Args:
            metadata: Email metadata
            email_id: Unique email identifier (email_000123)

        Returns:
            Path like: base_dir/by-date/2025/10/28/20251028_1444_sender_subject_000123.html
        """
        date = metadata.get('date')

        if isinstance(date, datetime):
            year = date.strftime('%Y')
            month = date.strftime('%m')
            day = date.strftime('%d')
        else:
            # Fallback for emails without valid date
            year = 'unknown'
            month = '00'
            day = '00'

        # Extract index from email_id (e.g., "email_000123" -> 123)
        try:
            email_index = int(email_id.split('_')[-1])
        except (ValueError, IndexError):
            email_index = 0

        # Generate human-readable filename
        filename = self.filename_gen.generate_filename(metadata, email_index)

        path = (
            self.base_dir
            / 'by-date'
            / year
            / month
            / day
            / filename
        )

        self.ensure_directory(path)
        return path
