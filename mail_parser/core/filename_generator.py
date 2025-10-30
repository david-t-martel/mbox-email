"""Generate human-readable filenames for emails."""

import re
from datetime import datetime
from typing import Any
from pathlib import Path


class FilenameGenerator:
    """Generate descriptive, human-readable filenames for emails."""

    @staticmethod
    def sanitize_for_filename(text: str, max_length: int = 50) -> str:
        """
        Sanitize text for use in filename.

        Args:
            text: Text to sanitize
            max_length: Maximum length

        Returns:
            Sanitized text safe for filenames
        """
        if not text:
            return "unknown"

        # Replace invalid characters with underscores
        # Invalid for both Windows and macOS: < > : " / \ | ? *
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)

        # Replace multiple spaces/underscores with single underscore
        sanitized = re.sub(r'[\s_]+', '_', sanitized)

        # Remove leading/trailing underscores and periods
        sanitized = sanitized.strip('_. ')

        # Truncate to max length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length].rstrip('_. ')

        # Ensure not empty
        if not sanitized:
            return "unknown"

        return sanitized

    @staticmethod
    def generate_filename(
        metadata: dict[str, Any],
        email_index: int,
        extension: str = 'html'
    ) -> str:
        """
        Generate human-readable filename.

        Format: YYYYMMDD_HHMM_sender_subject.html
        Example: 20251028_1444_john_doe_meeting_notes.html

        Args:
            metadata: Email metadata
            email_index: Email index number
            extension: File extension (default: html)

        Returns:
            Human-readable filename
        """
        # Extract date
        date_obj = metadata.get('date')
        if isinstance(date_obj, datetime):
            date_str = date_obj.strftime('%Y%m%d_%H%M')
        else:
            date_str = 'unknown_date'

        # Extract sender
        from_addr = metadata.get('from', {})
        sender_email = from_addr.get('email', 'unknown')
        sender_name = from_addr.get('name', '')

        # Use name if available, otherwise email username
        if sender_name:
            sender = FilenameGenerator.sanitize_for_filename(sender_name, max_length=20)
        elif '@' in sender_email:
            sender = sender_email.split('@')[0].lower()
            sender = FilenameGenerator.sanitize_for_filename(sender, max_length=20)
        else:
            sender = 'unknown'

        # Extract subject
        subject = metadata.get('subject', 'no_subject')
        subject = FilenameGenerator.sanitize_for_filename(subject, max_length=40)

        # Combine parts
        # Format: YYYYMMDD_HHMM_sender_subject_idx.html
        filename = f"{date_str}_{sender}_{subject}_{email_index:06d}.{extension}"

        return filename

    @staticmethod
    def generate_thread_filename(
        metadata: dict[str, Any],
        email_index: int,
        thread_position: int = 0,
        extension: str = 'html'
    ) -> str:
        """
        Generate filename for email in thread.

        Format: pos001_YYYYMMDD_HHMM_sender_subject.html
        Example: pos001_20251028_1444_john_doe_re_meeting.html

        Args:
            metadata: Email metadata
            email_index: Email index number
            thread_position: Position in thread (0-based)
            extension: File extension

        Returns:
            Thread-aware filename
        """
        base_filename = FilenameGenerator.generate_filename(
            metadata,
            email_index,
            extension
        )

        # Prepend thread position
        return f"pos{thread_position:03d}_{base_filename}"

    @staticmethod
    def extract_search_terms(metadata: dict[str, Any]) -> list[str]:
        """
        Extract searchable terms from metadata for indexing.

        Args:
            metadata: Email metadata

        Returns:
            List of search terms
        """
        terms = []

        # Sender info
        from_addr = metadata.get('from', {})
        if from_addr.get('name'):
            terms.append(from_addr['name'].lower())
        if from_addr.get('email'):
            terms.append(from_addr['email'].lower())
            # Add domain
            email = from_addr['email']
            if '@' in email:
                terms.append(email.split('@')[1].lower())

        # Subject
        subject = metadata.get('subject', '')
        if subject:
            # Split into words
            words = re.findall(r'\w+', subject.lower())
            terms.extend([w for w in words if len(w) > 2])  # Skip short words

        # Labels
        labels = metadata.get('gmail_labels', [])
        terms.extend([label.lower() for label in labels])

        # Date
        date_obj = metadata.get('date')
        if isinstance(date_obj, datetime):
            terms.extend([
                date_obj.strftime('%Y'),
                date_obj.strftime('%Y-%m'),
                date_obj.strftime('%B'),  # Month name
                date_obj.strftime('%A'),  # Day name
            ])

        return list(set(terms))  # Remove duplicates
