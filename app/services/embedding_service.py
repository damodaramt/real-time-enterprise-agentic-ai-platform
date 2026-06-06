import logging

from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)

model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


def generate_query_embedding(
    query: str
) -> list[float]:

    query = query.strip()

    if not query:
        raise ValueError(
            "Query cannot be empty."
        )

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    embedding_list = embedding.tolist()

    logger.info(
        "Generated query embedding. dimensions=%s",
        len(embedding_list)
    )

    return embedding_list
