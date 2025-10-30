"""Mbox index builder for O(1) email access."""

import logging
import sqlite3
import mmap
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from email import message_from_bytes
from email.message import Message
from tqdm import tqdm

logger = logging.getLogger(__name__)


@dataclass
class IndexStats:
    """Statistics from index building."""

    total_emails: int
    index_size_bytes: int
    build_time_seconds: float
    emails_per_second: float


class MboxIndexBuilder:
    """
    Build byte-offset index for mbox file to enable O(1) random access.

    The index maps email_id → (byte_offset, byte_length) and is stored in SQLite
    for fast lookups. Also extracts key metadata during indexing (thread_id,
    sender_domain, date) to enable efficient filtering.

    Performance: ~2 minutes to index 40K emails (one-time cost).
    """

    def __init__(self, mbox_path: str, index_db_path: str):
        """
        Initialize index builder.

        Args:
            mbox_path: Path to mbox file
            index_db_path: Path to SQLite index database
        """
        self.mbox_path = Path(mbox_path)
        self.index_db_path = Path(index_db_path)

        if not self.mbox_path.exists():
            raise FileNotFoundError(f"Mbox file not found: {mbox_path}")

        self.conn: Optional[sqlite3.Connection] = None

    def needs_rebuild(self) -> bool:
        """
        Check if index needs to be rebuilt.

        Returns:
            True if index is missing, outdated, or corrupted
        """
        if not self.index_db_path.exists():
            logger.info("Index does not exist, needs to be built")
            return True

        try:
            # Check if mbox file has been modified since index was created
            mbox_mtime = int(self.mbox_path.stat().st_mtime)

            conn = sqlite3.connect(str(self.index_db_path))
            cursor = conn.cursor()

            cursor.execute(
                "SELECT mbox_mtime, mbox_size FROM index_metadata WHERE mbox_path = ?",
                (str(self.mbox_path),)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                logger.info("Index metadata missing, needs rebuild")
                return True

            indexed_mtime, indexed_size = row
            current_size = self.mbox_path.stat().st_size

            if indexed_mtime != mbox_mtime:
                logger.info(f"Mbox file modified (mtime changed), needs rebuild")
                return True

            if indexed_size != current_size:
                logger.info(f"Mbox file size changed, needs rebuild")
                return True

            logger.info("Index is up-to-date")
            return False

        except Exception as e:
            logger.warning(f"Error checking index status: {e}, will rebuild")
            return True

    def build_index(self, show_progress: bool = True) -> IndexStats:
        """
        Build byte-offset index for mbox file.

        Scans the mbox file once, recording the byte offset and length of each
        email, along with key metadata for filtering. Uses memory-mapped file
        for performance.

        Args:
            show_progress: Show progress bar

        Returns:
            IndexStats with build statistics

        Performance: ~2 minutes for 40K emails
        """
        import time

        start_time = time.time()

        # Initialize database
        self._initialize_database()

        # Memory-map mbox file for fast scanning
        with open(self.mbox_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped:
                total_size = len(mmapped)

                # Find all email boundaries (lines starting with "From ")
                logger.info("Scanning mbox file for email boundaries...")
                boundaries = self._find_email_boundaries(mmapped, show_progress)

                logger.info(f"Found {len(boundaries):,} emails, extracting metadata...")

                # Extract metadata and build index
                batch_data = []
                batch_size = 1000

                pbar = tqdm(
                    total=len(boundaries),
                    desc="Building index",
                    unit="emails",
                    disable=not show_progress
                )

                for email_id, (start_offset, end_offset) in enumerate(boundaries):
                    byte_length = end_offset - start_offset

                    # Parse email to extract metadata
                    email_bytes = mmapped[start_offset:end_offset]
                    try:
                        message = message_from_bytes(email_bytes)
                        metadata = self._extract_index_metadata(message)
                    except Exception as e:
                        logger.warning(f"Failed to parse email {email_id}: {e}")
                        metadata = {}

                    batch_data.append((
                        email_id,
                        start_offset,
                        byte_length,
                        metadata.get('message_id'),
                        metadata.get('thread_id'),
                        metadata.get('date_timestamp'),
                        metadata.get('sender_domain'),
                        metadata.get('has_attachments', False),
                    ))

                    # Batch insert for performance
                    if len(batch_data) >= batch_size:
                        self._insert_batch(batch_data)
                        batch_data = []

                    pbar.update(1)

                # Insert remaining
                if batch_data:
                    self._insert_batch(batch_data)

                pbar.close()

                # Save metadata
                self._save_index_metadata(len(boundaries))

        # Calculate statistics
        build_time = time.time() - start_time
        index_size = self.index_db_path.stat().st_size

        stats = IndexStats(
            total_emails=len(boundaries),
            index_size_bytes=index_size,
            build_time_seconds=build_time,
            emails_per_second=len(boundaries) / build_time
        )

        logger.info(
            f"Index built: {stats.total_emails:,} emails in {stats.build_time_seconds:.1f}s "
            f"({stats.emails_per_second:.0f} emails/sec)"
        )

        return stats

    def get_email_location(self, email_id: int) -> tuple[int, int]:
        """
        Get byte offset and length for email.

        Args:
            email_id: Email ID

        Returns:
            Tuple of (byte_offset, byte_length)

        Performance: O(1) constant time lookup
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT byte_offset, byte_length FROM mbox_index WHERE email_id = ?",
            (email_id,)
        )

        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Email {email_id} not found in index")

        return row[0], row[1]

    def get_emails_by_thread(self, thread_id: str) -> list[int]:
        """
        Get all email IDs in a thread.

        Args:
            thread_id: Gmail thread ID (X-GM-THRID)

        Returns:
            List of email IDs

        Performance: O(log n) with index
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT email_id FROM mbox_index WHERE thread_id = ? ORDER BY email_id",
            (thread_id,)
        )

        return [row[0] for row in cursor.fetchall()]

    def get_emails_by_domain(self, domain: str) -> list[int]:
        """
        Get all email IDs from a sender domain.

        Args:
            domain: Sender domain (e.g., 'gmail.com')

        Returns:
            List of email IDs

        Performance: O(log n) with index
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT email_id FROM mbox_index WHERE sender_domain = ? ORDER BY email_id",
            (domain,)
        )

        return [row[0] for row in cursor.fetchall()]

    def get_emails_by_date_range(self, start: int, end: int) -> list[int]:
        """
        Get email IDs in a date range.

        Args:
            start: Start timestamp (Unix epoch)
            end: End timestamp (Unix epoch)

        Returns:
            List of email IDs

        Performance: O(log n) with index
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT email_id FROM mbox_index
            WHERE date_timestamp >= ? AND date_timestamp <= ?
            ORDER BY email_id
            """,
            (start, end)
        )

        return [row[0] for row in cursor.fetchall()]

    def get_all_email_ids(self) -> list[int]:
        """
        Get all email IDs in the index.

        Returns:
            List of all email IDs
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute("SELECT email_id FROM mbox_index ORDER BY email_id")

        return [row[0] for row in cursor.fetchall()]

    def get_total_emails(self) -> int:
        """
        Get total number of emails in index.

        Returns:
            Total email count
        """
        if not self.conn:
            self.conn = sqlite3.connect(str(self.index_db_path))

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mbox_index")

        return cursor.fetchone()[0]

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def _initialize_database(self) -> None:
        """Initialize SQLite database schema."""
        self.conn = sqlite3.connect(str(self.index_db_path))
        cursor = self.conn.cursor()

        # Drop existing tables for clean rebuild
        cursor.execute("DROP TABLE IF EXISTS mbox_index")
        cursor.execute("DROP TABLE IF EXISTS index_metadata")

        # Create index table
        cursor.execute("""
            CREATE TABLE mbox_index (
                email_id INTEGER PRIMARY KEY,
                byte_offset INTEGER NOT NULL,
                byte_length INTEGER NOT NULL,
                message_id TEXT,
                thread_id TEXT,
                date_timestamp INTEGER,
                sender_domain TEXT,
                has_attachments BOOLEAN
            )
        """)

        # Create indexes for fast filtering
        cursor.execute("CREATE INDEX idx_thread_id ON mbox_index(thread_id)")
        cursor.execute("CREATE INDEX idx_sender_domain ON mbox_index(sender_domain)")
        cursor.execute("CREATE INDEX idx_date ON mbox_index(date_timestamp)")

        # Create metadata table
        cursor.execute("""
            CREATE TABLE index_metadata (
                mbox_path TEXT PRIMARY KEY,
                mbox_size INTEGER,
                mbox_mtime INTEGER,
                total_emails INTEGER,
                index_created_at INTEGER,
                index_version TEXT
            )
        """)

        # Performance optimizations
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-64000")

        self.conn.commit()
        logger.info("Index database initialized")

    def _find_email_boundaries(
        self,
        mmapped: mmap.mmap,
        show_progress: bool
    ) -> list[tuple[int, int]]:
        """
        Find byte offsets of all email boundaries.

        Searches for lines starting with "From " which mark email boundaries
        in mbox format.

        Args:
            mmapped: Memory-mapped mbox file
            show_progress: Show progress bar

        Returns:
            List of (start_offset, end_offset) tuples
        """
        boundaries = []
        position = 0
        total_size = len(mmapped)

        # Check if file starts with "From "
        if mmapped[:5] == b'From ':
            boundaries.append(0)

        pbar = tqdm(
            total=total_size,
            desc="Scanning boundaries",
            unit="B",
            unit_scale=True,
            disable=not show_progress
        )

        # Find all "From " markers
        while True:
            position = mmapped.find(b'\nFrom ', position)
            if position == -1:
                break

            # Start of next email
            start_offset = position + 1
            boundaries.append(start_offset)
            position += 1
            pbar.update(position - pbar.n)

        pbar.close()

        # Convert to (start, end) pairs
        email_boundaries = []
        for i in range(len(boundaries)):
            start = boundaries[i]
            end = boundaries[i + 1] if i + 1 < len(boundaries) else total_size
            email_boundaries.append((start, end))

        return email_boundaries

    def _extract_index_metadata(self, message: Message) -> dict:
        """
        Extract metadata needed for index.

        Args:
            message: Email message

        Returns:
            Dictionary with metadata
        """
        from email.utils import parsedate_to_datetime

        metadata = {}

        # Message ID
        metadata['message_id'] = message.get('Message-ID', '').strip('<>')

        # Gmail thread ID (X-GM-THRID)
        metadata['thread_id'] = message.get('X-GM-THRID', '')

        # Date timestamp
        date_str = message.get('Date', '')
        if date_str:
            try:
                date_obj = parsedate_to_datetime(date_str)
                metadata['date_timestamp'] = int(date_obj.timestamp())
            except Exception:
                metadata['date_timestamp'] = None

        # Sender domain
        from_addr = message.get('From', '')
        if '@' in from_addr:
            # Extract domain from email
            try:
                email_part = from_addr.split('<')[1].split('>')[0] if '<' in from_addr else from_addr
                domain = email_part.split('@')[1].lower().strip()
                metadata['sender_domain'] = domain
            except Exception:
                metadata['sender_domain'] = 'unknown'

        # Has attachments (quick check)
        metadata['has_attachments'] = message.is_multipart()

        return metadata

    def _insert_batch(self, batch_data: list) -> None:
        """
        Batch insert index records.

        Args:
            batch_data: List of tuples to insert
        """
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO mbox_index (
                email_id, byte_offset, byte_length,
                message_id, thread_id, date_timestamp,
                sender_domain, has_attachments
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, batch_data)
        self.conn.commit()

    def _save_index_metadata(self, total_emails: int) -> None:
        """
        Save index metadata.

        Args:
            total_emails: Total number of emails indexed
        """
        import time

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO index_metadata (
                mbox_path, mbox_size, mbox_mtime, total_emails,
                index_created_at, index_version
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(self.mbox_path),
            self.mbox_path.stat().st_size,
            int(self.mbox_path.stat().st_mtime),
            total_emails,
            int(time.time()),
            '1.0'
        ))
        self.conn.commit()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
