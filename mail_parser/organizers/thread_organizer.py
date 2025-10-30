"""Organize emails by thread."""

from pathlib import Path
from typing import Any
import logging
from collections import defaultdict

from .base_organizer import BaseOrganizer
from ..core.filename_generator import FilenameGenerator

logger = logging.getLogger(__name__)


class ThreadOrganizer(BaseOrganizer):
    """Organize emails by Gmail thread ID."""

    def __init__(self, base_dir: Path):
        """Initialize with filename generator and thread tracking."""
        super().__init__(base_dir)
        self.filename_gen = FilenameGenerator()
        self.thread_positions = defaultdict(int)  # Track position in each thread

    def get_output_path(self, metadata: dict[str, Any], email_id: str) -> Path:
        """
        Get output path based on thread ID.

        Args:
            metadata: Email metadata
            email_id: Unique email identifier

        Returns:
            Path like: base_dir/by-thread/thread_1847237176990937209/pos001_20251028_1444_sender_subject.html
        """
        thread_id = metadata.get('gmail_thread_id', '')

        if thread_id:
            folder_name = f'thread_{thread_id}'
        else:
            # Use message ID as fallback
            msg_id = metadata.get('message_id', email_id)
            folder_name = f'single_{msg_id[:16]}'

        # Track position in thread
        position = self.thread_positions[folder_name]
        self.thread_positions[folder_name] += 1

        # Extract index from email_id
        try:
            email_index = int(email_id.split('_')[-1])
        except (ValueError, IndexError):
            email_index = 0

        # Generate thread-aware filename
        filename = self.filename_gen.generate_thread_filename(
            metadata,
            email_index,
            position
        )

        path = (
            self.base_dir
            / 'by-thread'
            / folder_name
            / filename
        )

        self.ensure_directory(path)
        return path
