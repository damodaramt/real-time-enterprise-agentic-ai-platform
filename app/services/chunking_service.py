from typing import List


CHUNK_SIZE = 500

CHUNK_OVERLAP = 50


def chunk_text(
    text: str
) -> List[str]:

    normalized = " ".join(
        text.split()
    )

    chunks = []

    start = 0

    while start < len(normalized):

        end = start + CHUNK_SIZE

        chunks.append(
            normalized[start:end]
        )

        start += (
            CHUNK_SIZE
            - CHUNK_OVERLAP
        )

    return chunks
