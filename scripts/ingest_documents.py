from __future__ import annotations

from pathlib import Path
from typing import List

import psycopg
from psycopg.types.json import Jsonb
from sentence_transformers import SentenceTransformer

from scripts.generate_embeddings import (
    DB_CONFIG,
    EMBEDDING_DIMENSION,
    MODEL_NAME,
    generate_embedding,
)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SUPPORTED_EXTENSIONS = {".txt", ".md"}
DOCUMENTS_DIR = Path("data/documents")


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Split text into overlapping chunks.
    """
    if not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks: List[str] = []
    start = 0
    step = chunk_size - chunk_overlap
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start += step

    return chunks


def insert_document_chunk(
    conn: psycopg.Connection,
    source: str,
    content: str,
    metadata: dict,
    embedding: List[float],
) -> str:
    """
    Insert one chunk into the documents table.
    """

    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected embedding dimension "
            f"{EMBEDDING_DIMENSION}, got {len(embedding)}"
        )

    vector_literal = (
        "[" +
        ",".join(
            f"{x:.10f}"
            for x in embedding
        ) +
        "]"
    )

    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO documents (
                content,
                metadata,
                embedding
            )
            VALUES (
                %s,
                %s,
                %s::vector
            )
            RETURNING id
            """,
            (
                content,
                Jsonb(metadata),
                vector_literal,
            ),
        )

        row = cur.fetchone()

        if row is None:
            raise RuntimeError(
                "Failed to insert document chunk"
            )

        document_id = str(row[0])

    conn.commit()

    return document_id


def process_file(
    conn: psycopg.Connection,
    model: SentenceTransformer,
    file_path: Path,
) -> int:
    """
    Read a file, chunk it, generate embeddings,
    and store in pgvector.
    """

    print(f"Processing file: {file_path}")

    text = file_path.read_text(
        encoding="utf-8"
    ).strip()

    if not text:
        print("Skipping empty file.")
        return 0

    chunks = chunk_text(text)

    print(
        f"Generated {len(chunks)} chunks."
    )

    inserted_count = 0

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        embedding = generate_embedding(
            model,
            chunk
        )

        metadata = {
            "source": file_path.name,
            "file_name": file_path.name,
            "file_path": str(file_path),
            "chunk_index": index,
            "total_chunks": len(chunks),
            "model": MODEL_NAME,
            "embedding_dimension": EMBEDDING_DIMENSION,
        }   

        document_id = insert_document_chunk(
            conn=conn,
            source=file_path.name,
            content=chunk,
            metadata=metadata,
            embedding=embedding,
        )

        print(
            f"Inserted chunk "
            f"{index}/{len(chunks)} "
            f"→ Document ID: "
            f"{document_id}"
        )

        inserted_count += 1

    return inserted_count


def main() -> None:

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Directory not found: "
            f"{DOCUMENTS_DIR}. "
            f"Create it and add "
            f".txt or .md files."
        )

    files = [
        path
        for path in DOCUMENTS_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower()
        in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise FileNotFoundError(
            f"No supported documents found "
            f"in {DOCUMENTS_DIR}. "
            f"Supported extensions: "
            f"{sorted(SUPPORTED_EXTENSIONS)}"
        )

    print(
        "Loading embedding model..."
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    total_inserted = 0

    print(
        "Connecting to PostgreSQL..."
    )

    with psycopg.connect(
        **DB_CONFIG
    ) as conn:

        for file_path in files:

            total_inserted += process_file(
                conn=conn,
                model=model,
                file_path=file_path,
            )

    print(
        "Document ingestion completed successfully."
    )

    print(
        f"Files processed: "
        f"{len(files)}"
    )

    print(
        f"Chunks inserted: "
        f"{total_inserted}"
    )


if __name__ == "__main__":
    main()
