# -*- coding: utf-8 -*-
"""
Main entry point for the crawler.
"""

import logging
from typing import List

from crawler.constants import DOUBAN_MOVIE_URL
from crawler.fetcher import PageFetcher
from crawler.models import Movie
from crawler.parser import MovieParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def crawl_douban_movies(max_pages: int = 1) -> List[Movie]:
    """
    Crawl Douban movie top 250.

    Args:
        max_pages: Maximum number of pages to crawl

    Returns:
        List of movies
    """
    all_movies = []
    fetcher = PageFetcher()
    current_url = DOUBAN_MOVIE_URL
    page_count = 0

    try:
        while current_url and page_count < max_pages:
            logger.info(f"Crawling page {page_count + 1}...")
            content = fetcher.fetch(current_url)

            if content is None:
                logger.error("Failed to fetch content, stopping")
                break

            movies, next_url = MovieParser.parse(content)
            all_movies.extend(movies)
            current_url = next_url
            page_count += 1

    finally:
        fetcher.close()

    logger.info(f"Total movies crawled: {len(all_movies)}")
    return all_movies


def main() -> None:
    """Main function."""
    logger.info("Starting Douban movie crawler...")
    movies = crawl_douban_movies(max_pages=1)

    if movies:
        logger.info("\n=== Top Movies ===")
        for i, movie in enumerate(movies[:10], 1):
            logger.info(f"{i}. {movie}")
    else:
        logger.warning("No movies found")


if __name__ == "__main__":
    main()
