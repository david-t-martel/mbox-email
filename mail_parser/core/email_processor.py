"""Email message processing and content extraction."""

import logging
from email.message import Message
from email import utils as email_utils
from datetime import datetime
from typing import Optional, Any
import chardet

logger = logging.getLogger(__name__)


class EmailProcessor:
    """Process and extract information from email messages."""

    @staticmethod
    def extract_metadata(message: Message) -> dict[str, Any]:
        """
        Extract metadata from email message.

        Args:
            message: Email message

        Returns:
            Dictionary containing email metadata
        """
        metadata = {
            'message_id': message.get('Message-ID', '').strip('<>'),
            'from': EmailProcessor.parse_address(message.get('From', '')),
            'to': EmailProcessor.parse_addresses(message.get('To', '')),
            'cc': EmailProcessor.parse_addresses(message.get('Cc', '')),
            'bcc': EmailProcessor.parse_addresses(message.get('Bcc', '')),
            'subject': EmailProcessor.decode_header(message.get('Subject', '')),
            'date': EmailProcessor.parse_date(message.get('Date', '')),
            'gmail_labels': EmailProcessor.get_labels(message),
            'gmail_thread_id': message.get('X-GM-THRID', ''),
            'has_attachments': EmailProcessor.has_attachments(message),
            'is_multipart': message.is_multipart(),
        }

        return metadata

    @staticmethod
    def parse_address(address: str) -> dict[str, str]:
        """
        Parse email address into name and email components.

        Args:
            address: Email address string

        Returns:
            Dictionary with 'name' and 'email' keys
        """
        if not address:
            return {'name': '', 'email': ''}

        try:
            name, email = email_utils.parseaddr(address)
            return {
                'name': EmailProcessor.decode_header(name),
                'email': email.lower().strip()
            }
        except Exception as e:
            logger.warning(f"Failed to parse address '{address}': {e}")
            return {'name': '', 'email': address}

    @staticmethod
    def parse_addresses(addresses: str) -> list[dict[str, str]]:
        """
        Parse multiple email addresses.

        Args:
            addresses: Comma-separated email addresses

        Returns:
            List of dictionaries with 'name' and 'email' keys
        """
        if not addresses:
            return []

        try:
            addr_list = email_utils.getaddresses([addresses])
            return [
                {
                    'name': EmailProcessor.decode_header(name),
                    'email': email.lower().strip()
                }
                for name, email in addr_list
            ]
        except Exception as e:
            logger.warning(f"Failed to parse addresses '{addresses}': {e}")
            return []

    @staticmethod
    def decode_header(header: str) -> str:
        """
        Decode email header that may contain encoded words.

        Args:
            header: Header string

        Returns:
            Decoded string
        """
        if not header:
            return ''

        try:
            from email.header import decode_header as email_decode_header
            decoded_parts = email_decode_header(header)
            result = []

            for content, encoding in decoded_parts:
                if isinstance(content, bytes):
                    if encoding:
                        result.append(content.decode(encoding, errors='replace'))
                    else:
                        # Try to detect encoding
                        detected = chardet.detect(content)
                        charset = detected.get('encoding', 'utf-8')
                        result.append(content.decode(charset, errors='replace'))
                else:
                    result.append(content)

            return ' '.join(result)
        except Exception as e:
            logger.warning(f"Failed to decode header '{header}': {e}")
            return str(header)

    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """
        Parse email date header.

        Args:
            date_str: Date string from email header

        Returns:
            Datetime object or None
        """
        if not date_str:
            return None

        try:
            # Parse RFC 2822 date
            date_tuple = email_utils.parsedate_to_datetime(date_str)
            return date_tuple
        except Exception as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return None

    @staticmethod
    def get_labels(message: Message) -> list[str]:
        """
        Extract Gmail labels from message.

        Args:
            message: Email message

        Returns:
            List of Gmail labels
        """
        labels_header = message.get('X-Gmail-Labels', '')
        if not labels_header:
            return []

        labels = [label.strip() for label in labels_header.split(',')]
        return [label for label in labels if label]

    @staticmethod
    def has_attachments(message: Message) -> bool:
        """
        Check if message has attachments.

        Args:
            message: Email message

        Returns:
            True if message has attachments
        """
        if not message.is_multipart():
            return False

        for part in message.walk():
            if part.get_content_disposition() == 'attachment':
                return True

        return False

    @staticmethod
    def extract_body(message: Message) -> dict[str, str]:
        """
        Extract email body content.

        Args:
            message: Email message

        Returns:
            Dictionary with 'text' and 'html' keys
        """
        body = {'text': '', 'html': ''}

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = part.get_content_disposition()

                # Skip attachments
                if content_disposition == 'attachment':
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue

                    # Detect encoding
                    charset = part.get_content_charset()
                    if not charset:
                        detected = chardet.detect(payload)
                        charset = detected.get('encoding', 'utf-8')

                    content = payload.decode(charset, errors='replace')

                    if content_type == 'text/plain':
                        body['text'] = content
                    elif content_type == 'text/html':
                        body['html'] = content

                except Exception as e:
                    logger.warning(f"Failed to extract part {content_type}: {e}")

        else:
            # Non-multipart message
            try:
                payload = message.get_payload(decode=True)
                if payload:
                    charset = message.get_content_charset()
                    if not charset:
                        detected = chardet.detect(payload)
                        charset = detected.get('encoding', 'utf-8')

                    content = payload.decode(charset, errors='replace')
                    content_type = message.get_content_type()

                    if content_type == 'text/html':
                        body['html'] = content
                    else:
                        body['text'] = content

            except Exception as e:
                logger.warning(f"Failed to extract body: {e}")

        return body

    @staticmethod
    def get_sender_domain(message: Message) -> str:
        """
        Extract sender's email domain.

        Args:
            message: Email message

        Returns:
            Sender's domain (e.g., 'gmail.com')
        """
        from_addr = EmailProcessor.parse_address(message.get('From', ''))
        email = from_addr.get('email', '')

        if '@' in email:
            return email.split('@')[1].lower()

        return 'unknown'
