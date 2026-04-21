from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.config import settings

if settings.QDRANT_URL:
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
    )
else:
    client = QdrantClient(
        url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
    )

COLLECTION_NAME = settings.QDRANT_COLLECTION
VECTOR_SIZE = 384


def create_collection():
    existing_collections = client.get_collections().collections
    existing_names = [collection.name for collection in existing_collections]

    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )


def recreate_collection():
    existing_collections = client.get_collections().collections
    existing_names = [collection.name for collection in existing_collections]

    if COLLECTION_NAME in existing_names:
        client.delete_collection(collection_name=COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )


def get_next_point_id() -> int:
    count_result = client.count(
        collection_name=COLLECTION_NAME,
        exact=True
    )
    return count_result.count


def upsert_chunks(chunks, embeddings, document_name="test.pdf"):
    create_collection()
    starting_id = get_next_point_id()

    points = []

    for index, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=starting_id + index,
                vector=vector,
                payload={
                    "document_name": document_name,
                    "text": chunk["text"],
                    "page": chunk["page"],
                    "chunk_index": chunk["chunk_index"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def search_similar_chunks(query_vector, limit=5):
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    formatted_results = []

    for point in response.points:
        payload = point.payload
        payload["score"] = point.score
        formatted_results.append(payload)

    return formatted_results


def get_knowledge_base_stats():
    create_collection()

    count_result = client.count(
        collection_name=COLLECTION_NAME,
        exact=True
    )

    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True,
        with_vectors=False
    )

    points = scroll_result[0]

    document_names = set()
    latest_document = None

    for point in points:
        payload = point.payload or {}
        doc_name = payload.get("document_name")

        if doc_name:
            document_names.add(doc_name)
            latest_document = doc_name

    return {
        "documents_loaded": len(document_names),
        "chunks_indexed": count_result.count,
        "last_uploaded_document": latest_document,
        "status": "Ready" if count_result.count > 0 else "Empty"
    }