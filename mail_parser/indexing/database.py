"""SQLite database with full-text search."""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailDatabase:
    """SQLite database for email indexing and search."""

    def __init__(self, db_path: str):
        """
        Initialize database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = None
        self.initialize_database()

    def initialize_database(self) -> None:
        """Initialize database schema."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Create emails table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT UNIQUE NOT NULL,
                message_id TEXT,
                thread_id TEXT,
                sender_name TEXT,
                sender_email TEXT,
                sender_domain TEXT,
                recipient_emails TEXT,
                subject TEXT,
                date TEXT,
                date_timestamp INTEGER,
                labels TEXT,
                has_attachments BOOLEAN,
                attachment_count INTEGER,
                html_path TEXT,
                content_hash TEXT,
                is_duplicate BOOLEAN,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create FTS5 virtual table for full-text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS emails_fts USING fts5(
                email_id UNINDEXED,
                subject,
                sender_email,
                sender_name,
                recipient_emails,
                labels,
                content='emails',
                content_rowid='id'
            )
        """)

        # Create triggers to keep FTS in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS emails_ai AFTER INSERT ON emails BEGIN
                INSERT INTO emails_fts(rowid, email_id, subject, sender_email, sender_name, recipient_emails, labels)
                VALUES (new.id, new.email_id, new.subject, new.sender_email, new.sender_name, new.recipient_emails, new.labels);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS emails_ad AFTER DELETE ON emails BEGIN
                DELETE FROM emails_fts WHERE rowid = old.id;
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS emails_au AFTER UPDATE ON emails BEGIN
                UPDATE emails_fts SET
                    subject = new.subject,
                    sender_email = new.sender_email,
                    sender_name = new.sender_name,
                    recipient_emails = new.recipient_emails,
                    labels = new.labels
                WHERE rowid = new.id;
            END
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sender_domain ON emails(sender_domain)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON emails(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_thread_id ON emails(thread_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_hash ON emails(content_hash)")

        self.conn.commit()
        logger.info(f"Database initialized: {self.db_path}")

    def insert_email(
        self,
        email_id: str,
        metadata: dict[str, Any],
        html_path: str,
        content_hash: str,
        is_duplicate: bool = False
    ) -> None:
        """
        Insert email into database.

        Args:
            email_id: Unique email identifier
            metadata: Email metadata
            html_path: Path to HTML file
            content_hash: Content hash
            is_duplicate: Whether email is a duplicate
        """
        try:
            cursor = self.conn.cursor()

            from_addr = metadata.get('from', {})
            to_addrs = metadata.get('to', [])
            date_obj = metadata.get('date')

            # Format date
            date_str = None
            date_timestamp = None
            if isinstance(date_obj, datetime):
                date_str = date_obj.isoformat()
                date_timestamp = int(date_obj.timestamp())

            # Combine recipient emails
            recipient_emails = ','.join([addr.get('email', '') for addr in to_addrs])

            # Combine labels
            labels = ','.join(metadata.get('gmail_labels', []))

            cursor.execute("""
                INSERT OR REPLACE INTO emails (
                    email_id, message_id, thread_id,
                    sender_name, sender_email, sender_domain,
                    recipient_emails, subject, date, date_timestamp,
                    labels, has_attachments, attachment_count,
                    html_path, content_hash, is_duplicate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email_id,
                metadata.get('message_id'),
                metadata.get('gmail_thread_id'),
                from_addr.get('name'),
                from_addr.get('email'),
                from_addr.get('email', '').split('@')[1] if '@' in from_addr.get('email', '') else '',
                recipient_emails,
                metadata.get('subject'),
                date_str,
                date_timestamp,
                labels,
                metadata.get('has_attachments', False),
                0,  # TODO: Add attachment count
                html_path,
                content_hash,
                is_duplicate
            ))

            self.conn.commit()

        except Exception as e:
            logger.error(f"Failed to insert email {email_id}: {e}")
            self.conn.rollback()

    def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0
    ) -> list[dict[str, Any]]:
        """
        Full-text search across emails.

        Args:
            query: Search query
            limit: Maximum results
            offset: Result offset for pagination

        Returns:
            List of matching emails
        """
        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT emails.*
                FROM emails
                JOIN emails_fts ON emails.id = emails_fts.rowid
                WHERE emails_fts MATCH ?
                ORDER BY rank
                LIMIT ? OFFSET ?
            """, (query, limit, offset))

            results = []
            for row in cursor.fetchall():
                results.append(dict(row))

            return results

        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return []

    def get_statistics(self) -> dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary of statistics
        """
        cursor = self.conn.cursor()

        # Total emails
        cursor.execute("SELECT COUNT(*) as count FROM emails")
        total = cursor.fetchone()['count']

        # Duplicates
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE is_duplicate = 1")
        duplicates = cursor.fetchone()['count']

        # With attachments
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE has_attachments = 1")
        with_attachments = cursor.fetchone()['count']

        # Unique domains
        cursor.execute("SELECT COUNT(DISTINCT sender_domain) as count FROM emails")
        unique_domains = cursor.fetchone()['count']

        # Unique threads
        cursor.execute("SELECT COUNT(DISTINCT thread_id) as count FROM emails WHERE thread_id IS NOT NULL")
        unique_threads = cursor.fetchone()['count']

        return {
            'total_emails': total,
            'duplicates': duplicates,
            'unique_emails': total - duplicates,
            'with_attachments': with_attachments,
            'unique_domains': unique_domains,
            'unique_threads': unique_threads,
        }

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
