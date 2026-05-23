import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()


def _validate_query(query: str) -> None:
    """Ensure the research query is valid before producing mock results."""
    if not query or not query.strip():
        raise ValueError("Search query must contain text.")


def _parse_search_item(item: Dict[str, Any]) -> Dict[str, str]:
    """Normalize a single search item into a clean dictionary."""
    return {
        "title": item.get("title", item.get("headline", "Untitled")),
        "url": item.get("url", item.get("link", "")),
        "snippet": item.get("snippet", item.get("summary", "")),
        "source": item.get("source", "local research"),
        "published_at": item.get("published_at", item.get("date", "")),
    }


def _summarize_results(results: List[Dict[str, str]]) -> str:
    """Create a brief, realistic summary of mock search results."""
    if not results:
        return "No research results were found."

    headlines = []
    for item in results[:5]:
        title = item.get("title", "Untitled")
        source = item.get("source", "local research")
        headlines.append(f"- {title} ({source})")

    return (
        "Simulated research briefing:\n"
        f"{len(results)} curated entries across market, strategy, and execution themes.\n"
        "Representative summaries:\n"
        + "\n".join(headlines)
    )


class TavilySearchClient:
    """Mock Tavily Search client for local demonstration purposes."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("TAVILY_API_KEY", "")
        self.base_url = base_url or os.getenv("TAVILY_API_URL", "mock://local")

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """Return mock search results for the requested topic."""
        _validate_query(query)

        sample_results = [
            {
                "title": f"Market momentum for {query}",
                "url": "https://example.com/research-1",
                "snippet": f"Early adoption is centered on operational teams that can integrate {query} into existing workflows with measurable KPIs.",
                "source": "Example Research Blog",
                "published_at": "2026-05-23",
            },
            {
                "title": f"Strategic planning implications of {query}",
                "url": "https://example.com/research-2",
                "snippet": f"Stakeholder alignment and pilot validation are emerging as critical success factors for projects involving {query}.",
                "source": "Research Insights Daily",
                "published_at": "2026-05-22",
            },
            {
                "title": f"Real-world use cases for {query}",
                "url": "https://example.com/research-3",
                "snippet": f"Teams are prioritizing use cases that deliver operational efficiency and faster decision cycles when exploring {query}.",
                "source": "Strategic Analysis Journal",
                "published_at": "2026-05-20",
            },
            {
                "title": f"Emerging adoption patterns in {query}",
                "url": "https://example.com/research-4",
                "snippet": f"A growing emphasis is placed on data governance and cross-team collaboration in deployments related to {query}.",
                "source": "Future Labs Review",
                "published_at": "2026-05-18",
            },
            {
                "title": f"Operational risks and opportunity areas for {query}",
                "url": "https://example.com/research-5",
                "snippet": f"Risk management, training, and change management are key considerations for business leaders reviewing {query}.",
                "source": "Research Operations Weekly",
                "published_at": "2026-05-15",
            },
        ]

        return [_parse_search_item(item) for item in sample_results[: min(limit, len(sample_results))]]

    def search_with_summary(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Return mock search results plus a summary string."""
        results = self.search(query=query, limit=limit)
        summary = _summarize_results(results)
        return {
            "query": query,
            "total_results": len(results),
            "results": results,
            "summary": summary,
        }


def run_tavily_search(query: str, limit: int = 5) -> Dict[str, Any]:
    """Convenience helper for quickly retrieving mock search data."""
    client = TavilySearchClient()
    return client.search_with_summary(query=query, limit=limit)
