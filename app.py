import json
import os
import urllib.request
from datetime import datetime

import streamlit as st


def get_api_url() -> str:
    """Return the backend research endpoint URL from secrets or environment."""
    try:
        return st.secrets.get("fastapi_url", "http://localhost:8000")
    except Exception:
        # Secrets file doesn't exist; use default or environment variable
        return os.getenv("FASTAPI_URL", "http://localhost:8000")



def call_research_api(topic: str) -> str:
    """Send the research topic to the FastAPI backend and return the generated report."""
    api_url = get_api_url().rstrip("/") + "/research"
    payload = json.dumps({"topic": topic}).encode("utf-8")
    request = urllib.request.Request(
        api_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
            return data.get("report", "No report returned from backend.")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        return f"Backend error {exc.code}: {error_body}"
    except urllib.error.URLError as exc:
        return f"Connection error: {exc.reason}"
    except Exception as exc:
        return f"Unexpected error: {exc}"


def render_header() -> None:
    st.set_page_config(
        page_title="AI Multi-Agent Research Assistant",
        page_icon="🤖",
        layout="wide",
    )

    st.title("AI Multi-Agent Research Assistant")
    st.markdown(
        "Use a research topic to trigger the workflow, generate a structured report, and download it as a text file."
    )
    st.markdown("---")


def render_input() -> tuple[str, bool]:
    topic = st.text_input(
        "Research topic",
        placeholder="Enter a topic like 'autonomous agent collaboration in research'",
    )
    run_button = st.button("Generate report")
    return topic.strip(), run_button


def render_report(report: str) -> None:
    if report:
        st.subheader("Generated Research Report")
        st.text_area("Report preview", report, height=360)

        report_bytes = report.encode("utf-8")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_filename = f"research_report_{timestamp}.txt"

        st.download_button(
            label="Download report as text file",
            data=report_bytes,
            file_name=download_filename,
            mime="text/plain",
        )


def main() -> None:
    render_header()

    report_container = st.container()
    topic, should_run = render_input()

    if should_run:
        if not topic:
            st.warning("Please enter a research topic before generating the report.")
            return

        with st.spinner("Loading workflow and generating your research report..."):
            report = call_research_api(topic)

        report_container.success("Research workflow complete.")
        render_report(report)

    if not should_run and "report" not in st.session_state:
        st.info("Enter a topic and click Generate report to start the workflow.")


if __name__ == "__main__":
    main()
