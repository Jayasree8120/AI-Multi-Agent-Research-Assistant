import os
from typing import Dict, List, Optional

from dotenv import load_dotenv

from tools.tavily_search import TavilySearchClient

load_dotenv()


class ResearchAgent:
    """Research Agent that collects trends, insights, and structured findings.

    This agent simulates a research workflow using local sample data instead of
    external search or AI APIs.
    """

    def __init__(self, tavily_client: Optional[TavilySearchClient] = None) -> None:
        self.tavily_client = tavily_client or TavilySearchClient()
        self.local_label = os.getenv("LOCAL_RESEARCH_LABEL", "Mock Research Agent")

    def execute(self, topic: str) -> str:
        """Run the research workflow and return structured research findings."""
        topic = topic.strip()
        if not topic:
            raise ValueError("Research topic must contain text.")

        search_results = self._gather_web_insights(topic)
        structured_findings = self._extract_insights(topic, search_results)

        return structured_findings

    def _gather_web_insights(self, topic: str) -> List[Dict[str, str]]:
        """Collect local mock research results for the topic."""
        search_query = f"Latest research trends and insights for {topic}"
        return self.tavily_client.search(query=search_query, limit=6)

    def _extract_insights(self, topic: str, sources: List[Dict[str, str]]) -> str:
        """Create a structured findings summary from mock search results."""
        if not sources:
            raise ValueError("No search results were returned from the local research client.")

        overview = (
            f"This mock research brief combines insights from {len(sources)} simulated sources to highlight current themes, "
            "practical considerations, and recommended next steps for the topic."
        )

        trends = self._build_trends_section(topic, sources)
        insights = self._build_insights_section(sources)
        data_preparation = self._build_data_preparation_section(sources)

        return (
            f"Research Topic: {topic}\n\n"
            f"Overview:\n{overview}\n\n"
            f"Key Trends:\n{trends}\n\n"
            f"Practical Insights:\n{insights}\n\n"
            f"Data Prepared for Summarization:\n{data_preparation}"
        )

    def _build_trends_section(self, topic: str, sources: List[Dict[str, str]]) -> str:
        """Build a trends section using the local source snippets."""
        return "\n".join([
            f"- Business teams are treating {topic} as a strategic capability rather than a one-off initiative.",
            "- Successful pilots are combining operational efficiency with clear performance metrics.",
            "- Cross-functional alignment and governance are emerging as the most important factors for scaled adoption.",
        ])

    def _build_insights_section(self, sources: List[Dict[str, str]]) -> str:
        """Turn source snippets into realistic research insights."""
        insights = [
            f"- {sources[0]['source']} highlights how operational leaders are evaluating {sources[0]['title'].split(' for ')[-1]} through measurable outcomes.",
            f"- {sources[1]['source']} calls out the importance of stakeholder engagement during planning and early validation.",
            f"- {sources[2]['source']} identifies efficiency gains as the leading commercial rationale for adoption.",
            f"- {sources[3]['source']} notes that successful teams balance technology, process, and people readiness.",
        ]
        return "\n".join(insights)

    def _build_data_preparation_section(self, sources: List[Dict[str, str]]) -> str:
        """Prepare notes to feed into the summarizer agent."""
        lines = []
        for idx, item in enumerate(sources, start=1):
            lines.append(
                f"- Source {idx}: {item['title']} | {item['snippet']}"
            )
        return "\n".join(lines)

