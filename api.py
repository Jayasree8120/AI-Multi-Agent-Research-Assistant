from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from agents.workflow import run_research_workflow

app = FastAPI(
    title="AI Multi-Agent Research Assistant API",
    description="Backend API for a mock local research workflow that demonstrates multi-agent orchestration without external APIs.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str = Field(
        ..., min_length=5, example="Emerging multi-agent strategies for research automation"
    )


class ResearchResponse(BaseModel):
    topic: str
    report: str
    summary: str
    source_notes: Optional[str] = Field(
        None, description="Internal research notes collected from the workflow"
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "message": "API is ready to accept research requests."}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty.")

    try:
        workflow_result = run_research_workflow(request.topic)
        return ResearchResponse(
            topic=workflow_result["topic"],
            report=workflow_result["report"],
            summary=workflow_result["summary"],
            source_notes=workflow_result.get("findings"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete the research workflow: {exc}",
        )
