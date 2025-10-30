"""High-performance streaming mbox parser."""

import mailbox
import logging
from pathlib import Path
from typing import Iterator, Optional
from email.message import Message
from tqdm import tqdm
import hashlib

logger = logging.getLogger(__name__)


class MboxParser:
    """Stream-based mbox parser optimized for large files."""

    def __init__(self, mbox_path: str, chunk_size: int = 1000):
        """
        Initialize mbox parser.

        Args:
            mbox_path: Path to the mbox file
            chunk_size: Number of emails to process in each chunk
        """
        self.mbox_path = Path(mbox_path)
        self.chunk_size = chunk_size

        if not self.mbox_path.exists():
            raise FileNotFoundError(f"Mbox file not found: {mbox_path}")

        logger.info(f"Initialized mbox parser for: {mbox_path}")
        logger.info(f"File size: {self.mbox_path.stat().st_size / (1024**3):.2f} GB")

    def count_messages(self) -> int:
        """
        Count total messages in mbox file.

        Returns:
            Total number of messages
        """
        logger.info("Counting messages in mbox file...")
        count = 0

        # Fast counting by looking for "From " lines
        with open(self.mbox_path, 'rb') as f:
            for line in f:
                if line.startswith(b'From '):
                    count += 1

        logger.info(f"Found {count:,} messages")
        return count

    def parse_stream(self, show_progress: bool = True) -> Iterator[tuple[int, Message]]:
        """
        Parse mbox file as a stream, yielding messages one at a time.

        Args:
            show_progress: Whether to show progress bar

        Yields:
            Tuple of (message_index, email.message.Message)
        """
        mbox = mailbox.mbox(str(self.mbox_path), create=False)

        total = None
        if show_progress:
            try:
                total = self.count_messages()
            except Exception as e:
                logger.warning(f"Could not count messages: {e}")

        with tqdm(total=total, desc="Parsing emails", unit="msg", disable=not show_progress) as pbar:
            for idx, message in enumerate(mbox):
                yield idx, message
                pbar.update(1)

    def parse_chunks(self, show_progress: bool = True) -> Iterator[list[tuple[int, Message]]]:
        """
        Parse mbox file in chunks for parallel processing.

        Args:
            show_progress: Whether to show progress bar

        Yields:
            List of tuples (message_index, email.message.Message)
        """
        chunk = []
        for idx, message in self.parse_stream(show_progress=show_progress):
            chunk.append((idx, message))

            if len(chunk) >= self.chunk_size:
                yield chunk
                chunk = []

        # Yield remaining messages
        if chunk:
            yield chunk

    @staticmethod
    def get_message_id(message: Message) -> str:
        """
        Get unique message ID.

        Args:
            message: Email message

        Returns:
            Unique message identifier
        """
        # Try to get Message-ID header
        msg_id = message.get('Message-ID', '')
        if msg_id:
            return msg_id.strip('<>')

        # Fall back to hash of key headers
        unique_str = ''.join([
            message.get('From', ''),
            message.get('To', ''),
            message.get('Subject', ''),
            message.get('Date', ''),
        ])

        return hashlib.md5(unique_str.encode()).hexdigest()

    @staticmethod
    def get_gmail_labels(message: Message) -> list[str]:
        """
        Extract Gmail labels from X-Gmail-Labels header.

        Args:
            message: Email message

        Returns:
            List of Gmail labels
        """
        labels_header = message.get('X-Gmail-Labels', '')
        if not labels_header:
            return []

        # Labels are comma-separated
        labels = [label.strip() for label in labels_header.split(',')]
        return [label for label in labels if label]

    @staticmethod
    def get_gmail_thread_id(message: Message) -> Optional[str]:
        """
        Extract Gmail thread ID from X-GM-THRID header.

        Args:
            message: Email message

        Returns:
            Gmail thread ID or None
        """
        return message.get('X-GM-THRID', None)

    @staticmethod
    def get_message_hash(message: Message) -> str:
        """
        Generate hash of message content for duplicate detection.

        Args:
            message: Email message

        Returns:
            MD5 hash of normalized content
        """
        # Normalize content for hashing
        content = ''.join([
            message.get('From', '').lower().strip(),
            message.get('Subject', '').lower().strip(),
            message.get('Date', '').strip(),
        ])

        # Add body content if available
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body = part.get_payload(decode=True)
                        if body:
                            content += body.decode('utf-8', errors='ignore').strip()
                            break
                    except Exception:
                        pass
        else:
            try:
                body = message.get_payload(decode=True)
                if body:
                    content += body.decode('utf-8', errors='ignore').strip()
            except Exception:
                pass

        return hashlib.md5(content.encode()).hexdigest()
