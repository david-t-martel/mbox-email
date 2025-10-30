"""Gmail API client with OAuth 2.0 authentication."""

import logging
import pickle
from pathlib import Path
from typing import Optional, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

logger = logging.getLogger(__name__)


class GmailClient:
    """Gmail API client for metadata enhancement."""

    # Gmail API scopes (read-only)
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(
        self,
        credentials_path: Optional[Path] = None,
        token_path: Optional[Path] = None,
        rate_limit_qps: int = 10,
    ):
        """
        Initialize Gmail API client.

        Args:
            credentials_path: Path to OAuth credentials JSON
            token_path: Path to save/load token
            rate_limit_qps: Rate limit (queries per second)
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.rate_limit_qps = rate_limit_qps
        self.last_request_time = 0

        self.service = None
        self.credentials = None

    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0.

        Returns:
            True if authentication successful
        """
        try:
            # Load existing token
            if self.token_path and self.token_path.exists():
                logger.info(f"Loading token from {self.token_path}")
                with open(self.token_path, 'rb') as token_file:
                    self.credentials = pickle.load(token_file)

            # Refresh or create new credentials
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    logger.info("Refreshing expired credentials")
                    self.credentials.refresh(Request())
                else:
                    if not self.credentials_path or not self.credentials_path.exists():
                        logger.error("Credentials file not found. Please provide credentials.json")
                        logger.info("Get credentials from: https://developers.google.com/gmail/api/quickstart/python")
                        return False

                    logger.info("Starting OAuth flow")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path),
                        self.SCOPES
                    )
                    self.credentials = flow.run_local_server(port=0)

                # Save token for future use
                if self.token_path:
                    self.token_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(self.token_path, 'wb') as token_file:
                        pickle.dump(self.credentials, token_file)
                    logger.info(f"Token saved to {self.token_path}")

            # Build service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            logger.info("Successfully authenticated with Gmail API")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        if self.rate_limit_qps <= 0:
            return

        min_interval = 1.0 / self.rate_limit_qps
        elapsed = time.time() - self.last_request_time

        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

        self.last_request_time = time.time()

    def get_message_metadata(self, message_id: str) -> Optional[dict[str, Any]]:
        """
        Get message metadata from Gmail API.

        Args:
            message_id: Gmail message ID

        Returns:
            Message metadata or None
        """
        if not self.service:
            logger.warning("Gmail service not initialized")
            return None

        try:
            self._rate_limit()

            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='metadata'
            ).execute()

            return self._extract_metadata(message)

        except HttpError as e:
            logger.warning(f"Failed to get message {message_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting message {message_id}: {e}")
            return None

    def get_thread_info(self, thread_id: str) -> Optional[dict[str, Any]]:
        """
        Get thread information from Gmail API.

        Args:
            thread_id: Gmail thread ID

        Returns:
            Thread information or None
        """
        if not self.service:
            logger.warning("Gmail service not initialized")
            return None

        try:
            self._rate_limit()

            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id,
                format='metadata'
            ).execute()

            return {
                'id': thread.get('id'),
                'snippet': thread.get('snippet', ''),
                'message_count': len(thread.get('messages', [])),
                'messages': [
                    self._extract_metadata(msg)
                    for msg in thread.get('messages', [])
                ],
            }

        except HttpError as e:
            logger.warning(f"Failed to get thread {thread_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting thread {thread_id}: {e}")
            return None

    def _extract_metadata(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Extract metadata from Gmail API response.

        Args:
            message: Gmail API message object

        Returns:
            Extracted metadata
        """
        metadata = {
            'id': message.get('id'),
            'thread_id': message.get('threadId'),
            'label_ids': message.get('labelIds', []),
            'snippet': message.get('snippet', ''),
            'internal_date': message.get('internalDate'),
        }

        # Extract headers if available
        if 'payload' in message and 'headers' in message['payload']:
            headers = {
                h['name']: h['value']
                for h in message['payload']['headers']
            }
            metadata['headers'] = headers

        return metadata

    def get_labels(self) -> list[dict[str, Any]]:
        """
        Get all Gmail labels.

        Returns:
            List of label dictionaries
        """
        if not self.service:
            logger.warning("Gmail service not initialized")
            return []

        try:
            self._rate_limit()

            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            return labels

        except HttpError as e:
            logger.error(f"Failed to get labels: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting labels: {e}")
            return []

    def search_messages(
        self,
        query: str,
        max_results: int = 100
    ) -> list[dict[str, Any]]:
        """
        Search messages using Gmail query syntax.

        Args:
            query: Gmail search query
            max_results: Maximum number of results

        Returns:
            List of message metadata
        """
        if not self.service:
            logger.warning("Gmail service not initialized")
            return []

        try:
            self._rate_limit()

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])

            return messages

        except HttpError as e:
            logger.error(f"Failed to search messages: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error searching messages: {e}")
            return []
