"""Command-line interface for mail parser."""

import click
import logging
import yaml
from pathlib import Path
from typing import Optional
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

from .core.mbox_parser import MboxParser
from .core.email_processor import EmailProcessor
from .core.mime_handler import MimeHandler
from .renderers.html_renderer import HtmlRenderer
from .organizers.date_organizer import DateOrganizer
from .organizers.domain_organizer import DomainOrganizer
from .organizers.thread_organizer import ThreadOrganizer
from .api.gmail_client import GmailClient
from .analysis.statistics import EmailStatistics
from .analysis.duplicate_detector import DuplicateDetector
from .indexing.database import EmailDatabase
from .dashboard.generator import DashboardGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MailParserCLI:
    """Main CLI application."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize CLI.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.stats = EmailStatistics()
        self.duplicate_detector = DuplicateDetector()
        self.html_renderer = HtmlRenderer()
        self.database: Optional[EmailDatabase] = None
        self.gmail_client: Optional[GmailClient] = None

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from YAML file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)

        # Default configuration
        return {
            'output': {
                'base_dir': './output',
                'organize_by': ['date', 'sender', 'thread'],
            },
            'performance': {
                'workers': min(8, cpu_count()),
                'chunk_size': 1000,
            },
            'gmail_api': {
                'enabled': False,
            },
            'analysis': {
                'enable_statistics': True,
                'enable_duplicate_detection': True,
            },
            'indexing': {
                'enable_full_text_search': True,
                'database_path': './output/email_index.db',
            },
        }

    def initialize_gmail_api(self) -> bool:
        """Initialize Gmail API client."""
        if not self.config['gmail_api'].get('enabled'):
            logger.info("Gmail API integration disabled")
            return False

        try:
            self.gmail_client = GmailClient(
                credentials_path=Path(self.config['gmail_api'].get('credentials_path', './credentials/credentials.json')),
                token_path=Path(self.config['gmail_api'].get('token_path', './credentials/token.json')),
                rate_limit_qps=self.config['gmail_api'].get('rate_limit_qps', 10),
            )

            return self.gmail_client.authenticate()

        except Exception as e:
            logger.error(f"Failed to initialize Gmail API: {e}")
            return False

    def initialize_database(self) -> bool:
        """Initialize database for indexing."""
        if not self.config['indexing'].get('enable_full_text_search'):
            logger.info("Database indexing disabled")
            return False

        try:
            db_path = self.config['indexing']['database_path']
            self.database = EmailDatabase(db_path)
            logger.info(f"Database initialized: {db_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False

    def process_email(
        self,
        idx: int,
        message,
        organizers: dict,
    ) -> dict:
        """
        Process single email.

        Args:
            idx: Email index
            message: Email message
            organizers: Dictionary of organizers

        Returns:
            Processing result
        """
        try:
            email_id = f"email_{idx:06d}"

            # Extract metadata
            metadata = EmailProcessor.extract_metadata(message)

            # Extract body
            body = EmailProcessor.extract_body(message)

            # Extract attachments
            attachments = MimeHandler.extract_attachments(message)

            # Get content hash for duplicate detection
            content_hash = MboxParser.get_message_hash(message)
            is_duplicate = self.duplicate_detector.is_duplicate(content_hash, email_id)

            # Render HTML
            html = self.html_renderer.render_email(message, metadata, body, attachments)

            # Save to all organized locations
            saved_paths = []
            for org_name, organizer in organizers.items():
                output_path = organizer.get_output_path(metadata, email_id)
                self.html_renderer.save_html(html, output_path)
                saved_paths.append(output_path)

            # Add to statistics
            self.stats.add_email(metadata, attachments)

            # Index in database
            if self.database:
                self.database.insert_email(
                    email_id,
                    metadata,
                    str(saved_paths[0]),
                    content_hash,
                    is_duplicate
                )

            return {
                'success': True,
                'email_id': email_id,
                'is_duplicate': is_duplicate,
                'paths': saved_paths,
            }

        except Exception as e:
            logger.error(f"Failed to process email {idx}: {e}")
            return {
                'success': False,
                'error': str(e),
            }

    def parse_mbox(
        self,
        mbox_path: str,
        limit: Optional[int] = None,
    ) -> None:
        """
        Parse mbox file and generate HTML emails.

        Args:
            mbox_path: Path to mbox file
            limit: Limit number of emails to process (for testing)
        """
        logger.info(f"Starting mbox parsing: {mbox_path}")

        # Initialize parser
        parser = MboxParser(
            mbox_path,
            chunk_size=self.config['performance']['chunk_size']
        )

        # Initialize organizers
        base_dir = Path(self.config['output']['base_dir'])
        organizers = {}

        for org_type in self.config['output']['organize_by']:
            if org_type == 'date':
                organizers['date'] = DateOrganizer(base_dir)
            elif org_type == 'sender':
                organizers['sender'] = DomainOrganizer(base_dir)
            elif org_type == 'thread':
                organizers['thread'] = ThreadOrganizer(base_dir)

        logger.info(f"Enabled organizers: {list(organizers.keys())}")

        # Process emails
        processed = 0
        errors = 0

        for idx, message in parser.parse_stream():
            # Check limit
            if limit and processed >= limit:
                logger.info(f"Reached limit of {limit} emails")
                break

            result = self.process_email(idx, message, organizers)

            if result['success']:
                processed += 1
            else:
                errors += 1

            # Progress update
            if processed % 100 == 0:
                logger.info(f"Processed {processed} emails...")

        logger.info(f"Processing complete: {processed} emails processed, {errors} errors")

        # Generate analytics
        if self.config['analysis'].get('enable_statistics'):
            summary = self.stats.get_summary()
            logger.info(f"Statistics: {summary}")

            # Generate HTML report
            report_path = base_dir / 'analytics_report.html'
            self.stats.generate_html_report(str(report_path))
            logger.info(f"Analytics report saved to {report_path}")

        # Duplicate summary
        if self.config['analysis'].get('enable_duplicate_detection'):
            dup_summary = self.duplicate_detector.get_summary()
            logger.info(f"Duplicates: {dup_summary['total_duplicates']} found")

        # Database statistics
        if self.database:
            db_stats = self.database.get_statistics()
            logger.info(f"Database stats: {db_stats}")

            # Generate interactive web dashboard
            logger.info("Generating interactive web dashboard...")
            dashboard = DashboardGenerator(
                base_dir,
                Path(self.config['indexing']['database_path'])
            )
            dashboard.generate()
            logger.info(f"✨ Dashboard ready! Open: {base_dir / 'index.html'}")


@click.group()
def cli():
    """Mail Parser - High-performance Gmail mbox parser and analyzer."""
    pass


@cli.command()
@click.option('--mbox', '-m', required=True, help='Path to mbox file')
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--config', '-c', help='Configuration file path')
@click.option('--limit', '-l', type=int, help='Limit number of emails (for testing)')
@click.option('--workers', '-w', type=int, default=8, help='Number of worker processes')
@click.option('--enable-gmail-api', is_flag=True, help='Enable Gmail API integration')
def parse(mbox, output, config, limit, workers, enable_gmail_api):
    """Parse mbox file and generate HTML emails."""
    app = MailParserCLI(config)

    # Override config with CLI args
    app.config['output']['base_dir'] = output
    app.config['performance']['workers'] = workers
    if enable_gmail_api:
        app.config['gmail_api']['enabled'] = True

    # Initialize components
    if app.config['gmail_api'].get('enabled'):
        app.initialize_gmail_api()

    app.initialize_database()

    # Parse mbox
    app.parse_mbox(mbox, limit)

    # Cleanup
    if app.database:
        app.database.close()


@cli.command()
@click.option('--config', '-c', help='Configuration file path')
def init(config):
    """Initialize Gmail API OAuth authentication."""
    app = MailParserCLI(config)
    app.config['gmail_api']['enabled'] = True

    success = app.initialize_gmail_api()

    if success:
        click.echo("✅ Gmail API authentication successful!")
        click.echo("Token saved for future use.")
    else:
        click.echo("❌ Gmail API authentication failed.")
        click.echo("Please check credentials and try again.")


@cli.command()
@click.option('--database', '-d', required=True, help='Path to database file')
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--limit', '-l', type=int, default=100, help='Maximum results')
def search(database, query, limit):
    """Search emails using full-text search."""
    db = EmailDatabase(database)

    results = db.search(query, limit=limit)

    click.echo(f"Found {len(results)} results for query: {query}\n")

    for result in results:
        click.echo(f"📧 {result['subject']}")
        click.echo(f"   From: {result['sender_email']}")
        click.echo(f"   Date: {result['date']}")
        click.echo(f"   Path: {result['html_path']}")
        click.echo()

    db.close()


@cli.command()
@click.option('--database', '-d', required=True, help='Path to database file')
def stats(database):
    """Show database statistics."""
    db = EmailDatabase(database)

    statistics = db.get_statistics()

    click.echo("📊 Database Statistics\n")
    for key, value in statistics.items():
        click.echo(f"{key}: {value:,}")

    db.close()


if __name__ == '__main__':
    cli()
