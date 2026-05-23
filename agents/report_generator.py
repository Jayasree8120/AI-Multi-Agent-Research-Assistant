import os

from dotenv import load_dotenv

load_dotenv()


def _build_report_text(topic: str, summary: str, insights: str) -> str:
    """Create a clean business-style report from summary and insight text."""
    return (
        f"Executive Summary:\n"
        f"This briefing summarizes a simulated research review for '{topic}', combining strategic observations with operational guidance.\n\n"
        f"Summary:\n{summary}\n\n"
        "Key Takeaways:\n"
        f"{insights}\n\n"
        "Strategic Considerations:\n"
        "- Clarify the most important risks and assumptions before moving from research to execution.\n"
        "- Ensure any pilot or initiative is aligned with broader business objectives.\n"
        "- Confirm that collaboration and governance structures are in place for adoption.\n\n"
        "Recommendations:\n"
        "- Prioritize the highest-value use cases and validate them through focused pilot work.\n"
        "- Use the findings to frame a short-term action plan for research and strategy teams.\n"
        "- Share this summary with stakeholders to align next-step decisions.\n\n"
        "Conclusion:\n"
        "The simulated process shown here illustrates how a modular research workflow can turn early insights into a concise, professional report suitable for business leaders."
    )


def _format_report_text(raw_text: str) -> str:
    """Return the generated report cleanly."""
    return raw_text.strip()


class ReportGeneratorAgent:
    """Report Generator Agent that converts summarized insights into a business-style report."""

    def __init__(self, model_name: str = "mock-report-generator") -> None:
        self.model_name = model_name

    def execute(self, topic: str, summary: str, insights: str) -> str:
        """Generate a professional report from summarized research content."""
        if not topic.strip():
            raise ValueError("Topic cannot be empty.")
        if not summary.strip():
            raise ValueError("Summary cannot be empty.")
        if not insights.strip():
            raise ValueError("Insights cannot be empty.")

        return _format_report_text(_build_report_text(topic, summary, insights))
