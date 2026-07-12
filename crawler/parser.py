# -*- coding: utf-8 -*-
"""
HTML parser for extracting data from web pages.
"""

import logging
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup

from crawler.constants import (
    DOUBAN_MOVIE_GRID,
    DOUBAN_MOVIE_ITEM,
    DOUBAN_MOVIE_TITLE,
    DOUBAN_NEXT_PAGE,
    DOUBAN_MOVIE_URL,
)
from crawler.models import Movie

logger = logging.getLogger(__name__)


class MovieParser:
    """Parser for extracting movie data from HTML."""

    @staticmethod
    def parse(html_content: bytes) -> Tuple[List[Movie], Optional[str]]:
        """
        Parse HTML content and extract movie information.

        Args:
            html_content: HTML content as bytes

        Returns:
            Tuple of (movie list, next page URL or None)
        """
        try:
            soup = BeautifulSoup(html_content, "lxml")
        except Exception as e:
            logger.error(f"Failed to parse HTML: {e}")
            return [], None

        movies = []

        try:
            movie_list_soup = soup.find("ol", attrs=DOUBAN_MOVIE_GRID)
            if not movie_list_soup:
                logger.warning("Movie grid not found in HTML")
                return movies, None

            for movie_li in movie_list_soup.find_all("li"):
                try:
                    detail = movie_li.find("div", attrs=DOUBAN_MOVIE_ITEM)
                    if not detail:
                        continue

                    title_elem = detail.find("span", attrs=DOUBAN_MOVIE_TITLE)
                    if not title_elem:
                        continue

                    movie_name = title_elem.get_text(strip=True)
                    movies.append(Movie(name=movie_name))
                    logger.debug(f"Extracted movie: {movie_name}")

                except Exception as e:
                    logger.warning(f"Error parsing movie item: {e}")
                    continue

            logger.info(f"Successfully extracted {len(movies)} movies")

        except Exception as e:
            logger.error(f"Error parsing movies: {e}")
            return movies, None

        # Extract next page URL
        next_page_url = None
        try:
            next_page = soup.find("span", attrs=DOUBAN_NEXT_PAGE)
            if next_page:
                next_link = next_page.find("a")
                if next_link and next_link.get("href"):
                    next_page_url = DOUBAN_MOVIE_URL + next_link["href"]
                    logger.info(f"Found next page: {next_page_url}")
        except Exception as e:
            logger.warning(f"Error extracting next page URL: {e}")

        return movies, next_page_url
