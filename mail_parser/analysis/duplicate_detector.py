"""Duplicate email detection."""

import logging
from typing import Any, Set
from collections import defaultdict

logger = logging.getLogger(__name__)


class DuplicateDetector:
    """Detect duplicate emails based on content hash."""

    def __init__(self):
        """Initialize duplicate detector."""
        self.seen_hashes: Set[str] = set()
        self.duplicates = defaultdict(list)
        self.duplicate_count = 0

    def is_duplicate(self, content_hash: str, email_id: str) -> bool:
        """
        Check if email is a duplicate based on content hash.

        Args:
            content_hash: MD5 hash of email content
            email_id: Unique email identifier

        Returns:
            True if email is a duplicate
        """
        if content_hash in self.seen_hashes:
            self.duplicates[content_hash].append(email_id)
            self.duplicate_count += 1
            return True

        self.seen_hashes.add(content_hash)
        return False

    def get_summary(self) -> dict[str, Any]:
        """
        Get duplicate detection summary.

        Returns:
            Dictionary with duplicate statistics
        """
        return {
            'total_duplicates': self.duplicate_count,
            'unique_emails': len(self.seen_hashes),
            'duplicate_groups': len(self.duplicates),
            'duplicate_hashes': dict(self.duplicates),
        }

    def get_duplicate_groups(self) -> list[dict[str, Any]]:
        """
        Get list of duplicate groups.

        Returns:
            List of duplicate groups
        """
        groups = []

        for content_hash, email_ids in self.duplicates.items():
            if len(email_ids) > 0:
                groups.append({
                    'hash': content_hash,
                    'count': len(email_ids) + 1,  # +1 for original
                    'email_ids': email_ids,
                })

        # Sort by count descending
        groups.sort(key=lambda x: x['count'], reverse=True)

        return groups
