from pydantic import BaseModel
from typing import List


class HealthResponse(BaseModel):
    status: str


class UploadResponse(BaseModel):
    success: bool
    file_name: str
    pages_processed: int
    chunks_stored: int


class SourceChunk(BaseModel):
    document_name: str
    page: int
    chunk_index: int
    text: str


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]