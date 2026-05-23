import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

DEFAULT_COLLECTION_NAME = "research_memory"


def _get_chroma_settings() -> Settings:
    """Build ChromaDB settings using environment variables."""
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chromadb_store")
    return Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)


def _get_client() -> chromadb.Client:
    """Initialize and return a ChromaDB client instance."""
    settings = _get_chroma_settings()
    return chromadb.Client(settings=settings)


def get_memory_collection(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    create_if_missing: bool = True,
) -> chromadb.api.models.Collection.Collection:
    """Get or create the Chroma collection for storing research memory."""
    client = _get_client()
    exists = any(col.name == collection_name for col in client.list_collections())
    if exists:
        return client.get_collection(name=collection_name)

    if create_if_missing:
        return client.create_collection(name=collection_name)

    raise ValueError(f"Collection '{collection_name}' does not exist.")


def store_research_memory(
    topic: str,
    report: str,
    metadata: Optional[Dict[str, Any]] = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> None:
    """Store a research topic and generated report into the memory collection."""
    if not topic.strip() or not report.strip():
        raise ValueError("Both topic and report are required to store memory.")

    collection = get_memory_collection(collection_name=collection_name)
    memory_id = f"research-{abs(hash(topic + report))}"
    metadata_payload = {
        "topic": topic,
        "summary": report[:220],
        **(metadata or {}),
    }

    collection.upsert(
        ids=[memory_id],
        documents=[report],
        metadatas=[metadata_payload],
    )


def retrieve_research_history(
    collection_name: str = DEFAULT_COLLECTION_NAME,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Retrieve the most recent research memory entries from ChromaDB."""
    if limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    collection = get_memory_collection(collection_name=collection_name)
    results = collection.get(include=["ids", "documents", "metadatas"])

    ids = results.get("ids", [])
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    entries: List[Dict[str, Any]] = []
    for idx, document in enumerate(documents[:limit]):
        metadata = metadatas[idx] if idx < len(metadatas) else {}
        entries.append(
            {
                "id": ids[idx] if idx < len(ids) else None,
                "topic": metadata.get("topic", ""),
                "summary": metadata.get("summary", ""),
                "report": document,
                "metadata": metadata,
            }
        )

    return entries


def search_memory(
    query: str,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Search the memory collection for relevant entries using a query."""
    if not query.strip():
        raise ValueError("Search query must contain text.")
    if limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    collection = get_memory_collection(collection_name=collection_name)
    results = collection.query(
        query_texts=[query],
        n_results=limit,
        include=["ids", "documents", "metadatas", "distances"],
    )

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    entries: List[Dict[str, Any]] = []
    for idx, document in enumerate(documents):
        metadata = metadatas[idx] if idx < len(metadatas) else {}
        entries.append(
            {
                "id": ids[idx] if idx < len(ids) else None,
                "topic": metadata.get("topic", ""),
                "summary": metadata.get("summary", ""),
                "report": document,
                "score": distances[idx] if idx < len(distances) else None,
                "metadata": metadata,
            }
        )

    return entries


def build_memory_preview(entries: List[Dict[str, Any]]) -> str:
    """Build a short preview text for retrieved memory entries."""
    if not entries:
        return "No previous research history found."

    lines = [
        f"- {entry['topic']} (summary: {entry['summary'][:100]})"
        for entry in entries[:5]
    ]
    return "Previous memory entries:\n" + "\n".join(lines)
