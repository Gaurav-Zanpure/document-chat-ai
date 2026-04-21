from sentence_transformers import SentenceTransformer
from app.config import settings

model = SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str):
    return model.encode(text).tolist()


def embed_texts(texts: list[str]):
    return model.encode(texts).tolist()