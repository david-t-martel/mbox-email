"""HTML email renderer with embedded styling."""

import logging
from pathlib import Path
from email.message import Message
from typing import Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup
import re

from ..core.email_processor import EmailProcessor
from ..core.mime_handler import MimeHandler

logger = logging.getLogger(__name__)


class HtmlRenderer:
    """Render emails as full HTML with embedded styling."""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize HTML renderer.

        Args:
            template_dir: Directory containing Jinja2 templates
        """
        if template_dir is None:
            template_dir = Path(__file__).parent / 'templates'

        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Add custom filters
        self.env.filters['format_size'] = MimeHandler.format_size
        self.env.filters['mime_icon'] = MimeHandler.get_mime_type_icon

    def render_email(
        self,
        message: Message,
        metadata: dict[str, Any],
        body: dict[str, str],
        attachments: list[dict[str, Any]],
    ) -> str:
        """
        Render email as HTML.

        Args:
            message: Email message
            metadata: Email metadata
            body: Email body (text and html)
            attachments: List of attachments

        Returns:
            HTML string
        """
        try:
            # Extract inline images
            inline_images = MimeHandler.extract_inline_images(message)

            # Process HTML body
            html_body = body.get('html', '')
            if html_body:
                html_body = self._process_html_body(html_body, inline_images)
            else:
                # Convert text to HTML
                html_body = self._text_to_html(body.get('text', ''))

            # Load template
            template = self.env.get_template('email.html')

            # Render
            html = template.render(
                metadata=metadata,
                body_html=html_body,
                attachments=attachments,
                inline_images=inline_images,
            )

            return html

        except Exception as e:
            logger.error(f"Failed to render email: {e}")
            return self._render_error(metadata, str(e))

    def _process_html_body(
        self,
        html: str,
        inline_images: list[dict[str, Any]]
    ) -> str:
        """
        Process HTML body to embed inline images.

        Args:
            html: HTML content
            inline_images: List of inline images

        Returns:
            Processed HTML
        """
        try:
            soup = BeautifulSoup(html, 'lxml')

            # Replace cid: references with base64 data URIs
            for img in inline_images:
                cid = img['content_id']
                if not cid:
                    continue

                # Find img tags with matching cid
                for img_tag in soup.find_all('img'):
                    src = img_tag.get('src', '')
                    if f'cid:{cid}' in src:
                        # Replace with base64 data URI
                        data_uri = f"data:{img['content_type']};base64,{img['base64']}"
                        img_tag['src'] = data_uri

            return str(soup)

        except Exception as e:
            logger.warning(f"Failed to process HTML body: {e}")
            return html

    def _text_to_html(self, text: str) -> str:
        """
        Convert plain text to HTML.

        Args:
            text: Plain text content

        Returns:
            HTML string
        """
        if not text:
            return '<p><em>No content</em></p>'

        # Escape HTML special characters
        from html import escape
        html = escape(text)

        # Convert URLs to links
        url_pattern = r'(https?://[^\s]+)'
        html = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', html)

        # Convert line breaks to <br>
        html = html.replace('\n', '<br>\n')

        # Wrap in div
        return f'<div class="text-body">{html}</div>'

    def _render_error(self, metadata: dict[str, Any], error: str) -> str:
        """
        Render error page.

        Args:
            metadata: Email metadata
            error: Error message

        Returns:
            HTML error page
        """
        try:
            template = self.env.get_template('error.html')
            return template.render(metadata=metadata, error=error)
        except Exception:
            return f"""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
    <h1>Error Rendering Email</h1>
    <p>{error}</p>
    <pre>{metadata}</pre>
</body>
</html>
"""

    def save_html(self, html: str, output_path: Path) -> None:
        """
        Save HTML to file.

        Args:
            html: HTML content
            output_path: Output file path
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            logger.debug(f"Saved HTML: {output_path}")

        except Exception as e:
            logger.error(f"Failed to save HTML to {output_path}: {e}")
