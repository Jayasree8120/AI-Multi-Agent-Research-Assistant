import os

from dotenv import load_dotenv

load_dotenv()


class SummarizerAgent:
    """Summarizer agent that creates a concise summary from mock research findings."""

    def __init__(self) -> None:
        self.summary_label = os.getenv("SUMMARY_LABEL", "Mock Summarizer")

    def execute(self, raw_findings: str) -> str:
        """Summarize findings into concise insights for final report generation."""
        if not raw_findings or not raw_findings.strip():
            raise ValueError("Research findings cannot be empty.")

        overview = self._extract_section(raw_findings, "Overview")
        trends = self._extract_section(raw_findings, "Key Trends")
        insights = self._extract_section(raw_findings, "Practical Insights")
        data_notes = self._extract_section(raw_findings, "Data Prepared for Summarization")

        summary_lines = [
            "Research Summary:",
            overview,
            "\nMajor Trends:",
            self._polish_section(trends),
            "\nKey Insights:",
            self._polish_section(insights),
            "\nActionable Notes:",
            self._polish_section(data_notes),
        ]
        return "\n".join(summary_lines)

    def _extract_section(self, text: str, heading: str) -> str:
        """Extract the content that follows a heading from the raw findings."""
        section_start = text.find(f"{heading}:\n")
        if section_start == -1:
            return "No additional details available."

        section_text = text[section_start + len(heading) + 2 :]
        next_heading_index = section_text.find("\n\n")
        if next_heading_index == -1:
            return section_text.strip()

        return section_text[:next_heading_index].strip()

    def _polish_section(self, section_text: str) -> str:
        """Turn section content into a concise, readable block."""
        lines = [line.strip() for line in section_text.splitlines() if line.strip()]
        if not lines:
            return "No additional details available."

        polished = []
        for line in lines:
            if line.startswith("-"):
                polished.append(line)
            else:
                polished.append(f"- {line}")

        return "\n".join(polished)
