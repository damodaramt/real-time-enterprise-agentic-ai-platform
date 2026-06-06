from typing import Dict
from typing import List
from typing import Set

import logging

logger = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 6000


def build_context(
    query: str,
    retrieved_documents: List[Dict]
) -> str:

    if not retrieved_documents:

        logger.warning(
            "No retrieved documents found"
        )

        return (
            "No relevant context found."
        )

    context_parts = []

    seen_chunks: Set[str] = set()

    total_chars = 0

    sorted_docs = sorted(
        retrieved_documents,
        key=lambda x: x.get(
            "score",
            0.0
        ),
        reverse=True
    )

    for index, doc in enumerate(
        sorted_docs,
        start=1
    ):

        content = doc.get(
            "content",
            ""
        ).strip()

        if not content:
            continue

        if content in seen_chunks:
            continue

        seen_chunks.add(content)

        source = doc.get(
            "source",
            "unknown"
        )

        score = round(
            float(
                doc.get(
                    "score",
                    0.0
                )
            ),
            4
        )

        chunk = (
            f"[DOCUMENT {index}]\n"
            f"Source: {source}\n"
            f"Score: {score}\n\n"
            f"{content}\n"
        )

        chunk_size = len(chunk)

        if (
            total_chars + chunk_size
            > MAX_CONTEXT_CHARS
        ):
            logger.info(
                "Context limit reached"
            )
            break

        context_parts.append(
            chunk
        )

        total_chars += chunk_size

    context = "\n".join(
        context_parts
    )

    prompt = f"""
You are an enterprise retrieval-augmented AI assistant.

Rules:

1. Use ONLY information found in CONTEXT.
2. Do not invent facts.
3. If answer is unavailable, respond:
   "I could not find the answer in the retrieved documents."
4. Cite document numbers when possible.

========================
CONTEXT
========================

{context}

========================
QUESTION
========================

{query}

========================
ANSWER
========================
"""

    logger.info(
        "Built context with %s chars",
        total_chars
    )

    return prompt.strip()
