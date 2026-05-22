import logging
from typing import Any
from typing import Dict
from typing import List

from psycopg.rows import dict_row
from psycopg.connection import Connection

from app.core.config import settings
from app.core.database import get_db_connection


logger = logging.getLogger(__name__)


def format_vector(
    embedding: List[float]
) -> str:

    return (
        "[" +
        ",".join(
            map(str, embedding)
        ) +
        "]"
    )


def clean_content(
    content: str
) -> str:

    cleaned_content = (
        content
        .replace("\\n", " ")
        .replace("\n", " ")
        .replace("\t", " ")
        .strip()
    )

    return " ".join(
        cleaned_content.split()
    )


def truncate_content(
    content: str
) -> str:

    cleaned_content = clean_content(
        content
    )

    if (
        len(cleaned_content)
        <= settings.MAX_CONTENT_LENGTH
    ):
        return cleaned_content

    return (
        cleaned_content[
            :settings.MAX_CONTENT_LENGTH
        ] + "..."
    )


def normalize_metadata(
    metadata: Dict[str, Any]
) -> Dict[str, Any]:

    if not metadata:
        return {}

    return {
        "source": metadata.get(
            "source"
        ),
        "chunk_index": metadata.get(
            "chunk_index"
        ),
        "embedding_dimension": metadata.get(
            "embedding_dimension"
        )
    }


def normalize_results(
    rows: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    normalized_results = []

    for row in rows:

        normalized_results.append(
            {
                "id": str(
                    row["id"]
                ),
                "content": truncate_content(
                    row["content"]
                ),
                "metadata": normalize_metadata(
                    row.get(
                        "metadata",
                        {}
                    )
                ),
                "distance": round(
                    float(
                        row["distance"]
                    ),
                    4
                )
            }
        )

    return normalized_results


def search_documents(
    query_embedding: List[float]
) -> List[Dict[str, Any]]:

    if not query_embedding:

        raise ValueError(
            "Query embedding is empty."
        )

    vector_string = format_vector(
        query_embedding
    )

    timeout_ms = int(
        settings.QUERY_TIMEOUT_SECONDS
        * 1000
    )

    connection: Connection = (
        get_db_connection()
    )

    try:

        with connection.cursor(
            row_factory=dict_row
        ) as cursor:

            cursor.execute(
                f"""
                SET statement_timeout = {timeout_ms};
                """
            )

            sql_query = """
            SELECT
                id,
                content,
                metadata,
                embedding <=> %s::vector AS distance
            FROM documents
            WHERE embedding <=> %s::vector < %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """

            cursor.execute(
                sql_query,
                (
                    vector_string,
                    vector_string,
                    settings.SIMILARITY_THRESHOLD,
                    vector_string,
                    settings.TOP_K_RESULTS
                )
            )

            rows = cursor.fetchall()

            logger.info(
                "Retrieved %s rows from semantic retrieval.",
                len(rows)
            )

            return normalize_results(
                rows
            )

    except Exception as error:

        logger.exception(
            "Semantic retrieval failed: %s",
            str(error)
        )

        raise

    finally:

        connection.close()
