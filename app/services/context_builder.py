from typing import Dict
from typing import List


MAX_CONTEXT_CHARS = 4000


def build_context(
    query: str,
    retrieved_documents: List[Dict]
) -> str:

    """
    Build optimized RAG prompt context.
    """

    if not retrieved_documents:

        return (
            "No relevant context found."
        )

    context_chunks = []

    total_length = 0

    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        content = document.get(
            "content",
            ""
        ).strip()

        if not content:

            continue

        chunk = (
            f"[Document {index}]\n"
            f"{content}\n"
        )

        chunk_size = len(chunk)

        if (
            total_length + chunk_size
            > MAX_CONTEXT_CHARS
        ):
            break

        context_chunks.append(
            chunk
        )

        total_length += chunk_size

    context_text = "\n".join(
        context_chunks
    )

    prompt = f"""
You are an enterprise AI assistant.

Answer ONLY using the provided context.

====================
CONTEXT
====================

{context_text}

====================
QUESTION
====================

{query}

====================
ANSWER
====================
"""

    return prompt.strip()
