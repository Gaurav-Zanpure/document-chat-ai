from sentence_transformers import SentenceTransformer
from app.config import settings

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str):
    model = get_model()
    return model.encode(text).tolist()


def embed_texts(texts: list[str]):
    model = get_model()
    return model.encode(texts).tolist()