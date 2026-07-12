# -*- coding: utf-8 -*-
"""
HTTP page fetcher with retry mechanism and error handling.
"""

import logging
from typing import Optional

import requests

from crawler.constants import DEFAULT_HEADERS, DEFAULT_RETRY, DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)


class PageFetcher:
    """Fetches web pages with automatic retry and error handling."""

    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        retry: int = DEFAULT_RETRY,
        headers: Optional[dict] = None,
    ) -> None:
        """
        Initialize the PageFetcher.

        Args:
            timeout: Request timeout in seconds
            retry: Number of retry attempts
            headers: Custom HTTP headers
        """
        self.timeout = timeout
        self.retry = retry
        self.headers = headers or DEFAULT_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch(self, url: str) -> Optional[bytes]:
        """
        Fetch page content with retry mechanism.

        Args:
            url: URL to fetch

        Returns:
            Page content as bytes, or None if all retries failed
        """
        for attempt in range(self.retry):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.retry})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                logger.info(f"✓ Successfully fetched: {url}")
                return response.content
            except requests.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.retry}")
            except requests.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}/{self.retry}")
            except requests.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}/{self.retry}: {e}")
            except requests.RequestException as e:
                logger.warning(f"Request error on attempt {attempt + 1}/{self.retry}: {e}")

        logger.error(f"✗ Failed to fetch {url} after {self.retry} attempts")
        return None

    def close(self) -> None:
        """Close the session."""
        self.session.close()
        logger.info("Fetcher session closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
