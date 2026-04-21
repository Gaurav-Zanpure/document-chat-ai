from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts
from app.services.qdrant_service import create_collection, upsert_chunks, get_knowledge_base_stats

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("")
def upload_pdfs(files: List[UploadFile] = File(...)):
    create_collection()

    uploaded_files = []
    total_pages = 0
    total_chunks = 0

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pages = extract_text_from_pdf(file_path)
        chunks = chunk_text(pages)
        texts = [chunk["text"] for chunk in chunks]

        embeddings = embed_texts(texts)
        upsert_chunks(chunks, embeddings, document_name=file.filename)

        uploaded_files.append(file.filename)
        total_pages += len(pages)
        total_chunks += len(chunks)

    stats = get_knowledge_base_stats()

    return {
        "message": "Files uploaded and processed successfully",
        "uploaded_files": uploaded_files,
        "files_count": len(uploaded_files),
        "pages_processed": total_pages,
        "chunks_added": total_chunks,
        "knowledge_base": stats
    }