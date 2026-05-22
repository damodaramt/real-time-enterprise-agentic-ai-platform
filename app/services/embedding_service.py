from sentence_transformers import (
    SentenceTransformer
)

from app.core.config import settings


model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


def generate_query_embedding(
    query: str
):

    embedding = model.encode(query)

    return embedding.tolist()
