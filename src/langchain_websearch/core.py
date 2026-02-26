"""
Core components for LangChain WebSearch Tool.
"""

from typing import List

from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class SearchResult(BaseModel):
    """Search result model."""

    title: str
    link: str
    snippet: str
    display_link: str
    position: int


class WebSearchTool(BaseTool):
    """LangChain tool for web search functionality using Querit Search API."""

    name: str = "web_search"
    description: str = (
        "A tool for searching the web using Querit Search API. "
        "Useful for finding up-to-date information, news, and facts. "
        "Input should be a search query string."
    )

    num_results: int = Field(default=10, ge=1, le=50)
    region: str = Field(default="en-US")  # 保留但不使用
    safe_search: bool = Field(default=True)  # 保留但不使用

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 延迟导入以避免循环导入
        from .querit_search import QueritSearchBackend

        self._backend_instance = QueritSearchBackend()

    def _run(self, query: str) -> str:
        """Execute the search and return formatted results."""
        try:
            results = self._backend_instance.search(
                query=query, num_results=self.num_results
            )

            if not results:
                return "No search results found."

            return self._format_results(results)

        except Exception as e:
            return f"Search failed: {str(e)}"

    def _format_results(self, results: List[SearchResult]) -> str:
        """Format search results into a readable string."""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result.title}")
            formatted.append(f"   URL: {result.link}")
            formatted.append(f"   Preview: {result.snippet}")
            formatted.append("")

        return "\n".join(formatted)

    async def _arun(self, query: str) -> str:
        """Async version of the search tool."""
        return self._run(query)
