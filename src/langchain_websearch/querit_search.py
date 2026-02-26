"""
Querit Search backend implementation.
"""

import os
import requests
from typing import List, Optional

from .core import SearchResult


class QueritSearchBackend:
    """Querit Search API backend."""

    BASE_URL = "https://api.querit.ai/v1/search"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("QUERIT_API_KEY")

    def validate_credentials(self) -> bool:
        """Validate Querit API credentials."""
        return bool(self.api_key)

    def search(self, query: str, num_results: int = 10, **kwargs) -> List[SearchResult]:
        """Perform search using Querit Search API."""
        if not self.validate_credentials():
            raise ValueError(
                "Querit API key not found. "
                "Please set QUERIT_API_KEY environment variable."
            )

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {"query": query}

        response = requests.post(
            self.BASE_URL, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()

        data = response.json()

        results = []

        if "results" in data and "result" in data["results"]:
            for i, item in enumerate(data["results"]["result"]):
                result = SearchResult(
                    title=item.get("title", ""),
                    link=item.get("url", ""),
                    snippet=item.get("snippet", ""),
                    display_link=item.get("site_name", ""),
                    position=i + 1,
                )
                results.append(result)

        return results[
            :num_results
        ]  # Ensure we return only requested number of results
