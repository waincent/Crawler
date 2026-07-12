# -*- coding: utf-8 -*-
"""
Data models for crawler.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """Movie data model."""

    name: str
    rating: Optional[float] = None
    url: Optional[str] = None

    def __str__(self) -> str:
        rating_str = f" ({self.rating})" if self.rating else ""
        return f"{self.name}{rating_str}"
