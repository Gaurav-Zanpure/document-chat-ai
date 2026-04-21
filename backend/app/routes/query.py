from fastapi import APIRouter

from app.models.schemas import QueryRequest, QueryResponse, SourceChunk
from app.services.rag_service import generate_answer

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    result = generate_answer(request.question)

    sources = [
        SourceChunk(
            document_name=source.get("document_name", "unknown"),
            page=source.get("page", 0),
            chunk_index=source.get("chunk_index", 0),
            text=source.get("text", "")
        )
        for source in result["sources"]
    ]

    return QueryResponse(
        answer=result["answer"],
        sources=sources
    )