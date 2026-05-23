from .researcher import ResearchAgent
from .summarizer import SummarizerAgent
from .report_generator import ReportGeneratorAgent
from memory.chroma_store import store_research_memory


def run_research_workflow(topic: str) -> dict[str, str]:
    """Execute the full research workflow and persist the final report."""
    research_agent = ResearchAgent()
    summarizer_agent = SummarizerAgent()
    report_agent = ReportGeneratorAgent()

    raw_findings = research_agent.execute(topic)
    summary = summarizer_agent.execute(raw_findings)
    report = report_agent.execute(topic, summary, raw_findings)

    try:
        store_research_memory(
            topic=topic,
            report=report,
            metadata={"summary": summary},
        )
    except Exception:
        # Memory storage should not stop the workflow, but log or handle as needed.
        pass

    return {
        "topic": topic,
        "findings": raw_findings,
        "summary": summary,
        "report": report,
    }
