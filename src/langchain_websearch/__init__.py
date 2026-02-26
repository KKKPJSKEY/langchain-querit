"""
LangChain WebSearch Tool
A powerful search tool for LangChain using Querit Search API.
"""

from .core import WebSearchTool, SearchResult
from .querit_search import QueritSearchBackend

__version__ = "0.0.2"
__all__ = ["WebSearchTool", "SearchResult", "QueritSearchBackend"]
