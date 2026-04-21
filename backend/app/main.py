from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.query import router as query_router
from app.models.schemas import HealthResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts
from app.services.qdrant_service import recreate_collection, upsert_chunks, get_knowledge_base_stats
from app.services.rag_service import generate_answer

app = FastAPI(
    title="Document Chat AI Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")


@app.get("/test-pdf")
def test_pdf():
    pages = extract_text_from_pdf("test.pdf")
    chunks = chunk_text(pages)

    return {
        "pages": len(pages),
        "chunks": len(chunks),
        "sample_chunks": chunks[:3]
    }


@app.get("/test-store")
def test_store():
    pages = extract_text_from_pdf("test.pdf")
    chunks = chunk_text(pages)
    texts = [chunk["text"] for chunk in chunks]

    recreate_collection()
    embeddings = embed_texts(texts)
    upsert_chunks(chunks, embeddings, document_name="test.pdf")

    return {
        "message": "Chunks embedded and stored successfully",
        "pages": len(pages),
        "chunks": len(chunks)
    }


@app.get("/test-answer")
def test_answer(question: str = "What is the statement date?"):
    result = generate_answer(question)

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }


@app.get("/kb-status")
def kb_status():
    return get_knowledge_base_stats()


app.include_router(upload_router)
app.include_router(query_router)