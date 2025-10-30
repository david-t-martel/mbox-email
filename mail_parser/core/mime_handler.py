"""MIME content and attachment handling."""

import logging
import base64
import mimetypes
from email.message import Message
from pathlib import Path
from typing import Optional, Any
import chardet

logger = logging.getLogger(__name__)


class MimeHandler:
    """Handle MIME content and attachments."""

    @staticmethod
    def extract_attachments(message: Message) -> list[dict[str, Any]]:
        """
        Extract all attachments from email message.

        Args:
            message: Email message

        Returns:
            List of attachment dictionaries
        """
        attachments = []

        if not message.is_multipart():
            return attachments

        for part in message.walk():
            content_disposition = part.get_content_disposition()

            if content_disposition != 'attachment':
                continue

            attachment = MimeHandler._extract_attachment_info(part)
            if attachment:
                attachments.append(attachment)

        return attachments

    @staticmethod
    def _extract_attachment_info(part: Message) -> Optional[dict[str, Any]]:
        """
        Extract information about an attachment.

        Args:
            part: MIME part

        Returns:
            Dictionary with attachment information
        """
        try:
            filename = part.get_filename()
            if not filename:
                filename = 'unnamed_attachment'

            # Decode filename if necessary
            from email.header import decode_header
            decoded_filename = decode_header(filename)[0]
            if isinstance(decoded_filename[0], bytes):
                filename = decoded_filename[0].decode(
                    decoded_filename[1] or 'utf-8',
                    errors='replace'
                )
            else:
                filename = decoded_filename[0]

            payload = part.get_payload(decode=True)
            if not payload:
                return None

            content_type = part.get_content_type()
            size = len(payload)

            return {
                'filename': filename,
                'content_type': content_type,
                'size': size,
                'data': payload,  # Binary data
                'base64': base64.b64encode(payload).decode('ascii'),
            }

        except Exception as e:
            logger.warning(f"Failed to extract attachment: {e}")
            return None

    @staticmethod
    def save_attachment(attachment: dict[str, Any], output_dir: Path) -> Optional[Path]:
        """
        Save attachment to disk.

        Args:
            attachment: Attachment dictionary
            output_dir: Directory to save attachment

        Returns:
            Path to saved file or None
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)

            filename = attachment['filename']
            filepath = output_dir / filename

            # Handle duplicate filenames
            counter = 1
            while filepath.exists():
                name = Path(filename).stem
                ext = Path(filename).suffix
                filepath = output_dir / f"{name}_{counter}{ext}"
                counter += 1

            with open(filepath, 'wb') as f:
                f.write(attachment['data'])

            logger.debug(f"Saved attachment: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save attachment '{attachment.get('filename')}': {e}")
            return None

    @staticmethod
    def is_image(content_type: str) -> bool:
        """
        Check if content type is an image.

        Args:
            content_type: MIME content type

        Returns:
            True if content type is an image
        """
        return content_type.startswith('image/')

    @staticmethod
    def extract_inline_images(message: Message) -> list[dict[str, Any]]:
        """
        Extract inline images from email message.

        Args:
            message: Email message

        Returns:
            List of inline image dictionaries
        """
        images = []

        if not message.is_multipart():
            return images

        for part in message.walk():
            content_type = part.get_content_type()

            # Check for inline images
            if not MimeHandler.is_image(content_type):
                continue

            content_disposition = part.get_content_disposition()
            content_id = part.get('Content-ID', '')

            # Only include inline images
            if content_disposition == 'attachment':
                continue

            try:
                payload = part.get_payload(decode=True)
                if not payload:
                    continue

                # Remove < > from Content-ID
                cid = content_id.strip('<>')

                images.append({
                    'content_id': cid,
                    'content_type': content_type,
                    'size': len(payload),
                    'data': payload,
                    'base64': base64.b64encode(payload).decode('ascii'),
                })

            except Exception as e:
                logger.warning(f"Failed to extract inline image: {e}")

        return images

    @staticmethod
    def get_mime_type_icon(content_type: str) -> str:
        """
        Get icon/emoji for MIME type.

        Args:
            content_type: MIME content type

        Returns:
            Icon string
        """
        icons = {
            'application/pdf': '📄',
            'application/zip': '📦',
            'application/x-zip-compressed': '📦',
            'image/': '🖼️',
            'video/': '🎥',
            'audio/': '🎵',
            'text/': '📝',
            'application/msword': '📃',
            'application/vnd.ms-excel': '📊',
            'application/vnd.ms-powerpoint': '📽️',
        }

        for key, icon in icons.items():
            if content_type.startswith(key):
                return icon

        return '📎'

    @staticmethod
    def format_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024

        return f"{size_bytes:.1f} TB"
