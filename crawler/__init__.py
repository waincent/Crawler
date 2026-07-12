"""
Crawler - A web crawler framework with support for multiple data sources.
"""

__version__ = "0.1.0"
__author__ = "waincent"

from crawler.fetcher import PageFetcher
from crawler.parser import MovieParser

__all__ = ["PageFetcher", "MovieParser"]
