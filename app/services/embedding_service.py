from sentence_transformers import SentenceTransformer

from app.core.config import settings


model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


def generate_query_embedding(
    query: str
) -> list[float]:

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()
