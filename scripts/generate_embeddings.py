from __future__ import annotations

import os
from typing import Any, List
from uuid import UUID

import psycopg
from psycopg.types.json import Jsonb
from sentence_transformers import SentenceTransformer


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": int(os.getenv("POSTGRES_PORT", "5434")),
    "dbname": os.getenv("POSTGRES_DB", "enterprise_ai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


def generate_embedding(
    model: SentenceTransformer,
    text: str,
) -> List[float]:
    """
    Generate a 384-dimensional embedding vector.
    """
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def insert_document(
    conn: psycopg.Connection,
    source: str,
    content: str,
    metadata: dict[str, Any],
    embedding: List[float],
) -> UUID:
    """
    Insert a document and its embedding into the documents table.

    Expected schema:
        documents (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata JSONB,
            embedding VECTOR(384) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """
    if not source.strip():
        raise ValueError("source must not be empty")

    if not content.strip():
        raise ValueError("content must not be empty")

    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected embedding dimension "
            f"{EMBEDDING_DIMENSION}, got {len(embedding)}"
        )

    # pgvector expects a literal like:
    # [0.1,0.2,0.3,...]
    vector_literal = "[" + ",".join(f"{x:.10f}" for x in embedding) + "]"

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (
                source,
                content,
                metadata,
                embedding
            )
            VALUES (
                %s,
                %s,
                %s,
                %s::vector
            )
            RETURNING id
            """,
            (
                source,
                content,
                Jsonb(metadata),
                vector_literal,
            ),
        )
        row = cur.fetchone()

        if row is None:
            raise RuntimeError("Failed to insert document")

        document_id = row[0]

    conn.commit()
    return document_id


def main() -> None:
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    source = "sample"

    sample_text = """
    Enterprise Agentic AI platforms combine FastAPI, Kafka,
    AWS Lambda, PostgreSQL pgvector, RAG, MCP, and Langfuse.
    """.strip()

    print("Generating embedding...")
    embedding = generate_embedding(model, sample_text)

    print(f"Embedding dimension: {len(embedding)}")

    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected {EMBEDDING_DIMENSION}, got {len(embedding)}"
        )

    metadata = {
        "source": source,
        "model": MODEL_NAME,
        "embedding_dimension": EMBEDDING_DIMENSION,
        "frameworks": [
            "FastAPI",
            "Kafka",
            "AWS Lambda",
            "PostgreSQL",
            "pgvector",
            "RAG",
            "MCP",
            "Langfuse",
        ],
    }

    print("Connecting to PostgreSQL...")
    with psycopg.connect(**DB_CONFIG) as conn:
        print("Inserting document into pgvector...")
        document_id = insert_document(
            conn=conn,
            source=source,
            content=sample_text,
            metadata=metadata,
            embedding=embedding,
        )

    print("Embedding stored successfully.")
    print(f"Document ID: {document_id}")


if __name__ == "__main__":
    main()
