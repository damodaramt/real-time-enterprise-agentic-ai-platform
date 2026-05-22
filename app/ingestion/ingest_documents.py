import uuid
from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.database import get_db_connection


CHUNK_SIZE = 500


model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


def chunk_text(
    text: str
) -> List[str]:

    cleaned = " ".join(
        text.split()
    )

    chunks = []

    for index in range(
        0,
        len(cleaned),
        CHUNK_SIZE
    ):

        chunk = cleaned[
            index:index + CHUNK_SIZE
        ]

        if chunk.strip():

            chunks.append(chunk)

    return chunks


def generate_embedding(
    text: str
) -> List[float]:

    embedding = model.encode(
        text
    )

    return embedding.tolist()


def insert_document(
    content: str,
    metadata: dict,
    embedding: List[float]
) -> None:

    vector = (
        "[" +
        ",".join(
            map(str, embedding)
        ) +
        "]"
    )

    connection = get_db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO documents (
                    id,
                    content,
                    metadata,
                    embedding
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s::vector
                );
                """,
                (
                    str(uuid.uuid4()),
                    content,
                    metadata,
                    vector
                )
            )

            connection.commit()

    finally:

        connection.close()


def ingest_text_file(
    file_path: str
) -> None:

    path = Path(file_path)

    text = path.read_text(
        encoding="utf-8"
    )

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(
            chunk
        )

        insert_document(
            content=chunk,
            metadata={
                "source": path.name,
                "chunk_index": index,
                "embedding_dimension": 384
            },
            embedding=embedding
        )

    print(
        f"Ingested {len(chunks)} chunks."
    )


if __name__ == "__main__":

    ingest_text_file(
        "data/sample.txt"
    )
