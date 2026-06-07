import logging

logger = logging.getLogger(__name__)


def build_prompt(
    query: str,
    context: str,
) -> str:

    if not isinstance(query, str):
        raise TypeError(
            "Query must be a string."
        )

    if not isinstance(context, str):
        raise TypeError(
            "Context must be a string."
        )

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if not context.strip():
        context = (
            "No relevant context found."
        )

    prompt = f"""
You are an enterprise retrieval-augmented AI assistant.

Rules:

1. Use ONLY information found in CONTEXT.
2. Do not invent facts.
3. If answer is unavailable, respond:
   "I could not find the answer in the retrieved documents."
4. Be concise and accurate.

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
        "Prompt built successfully."
    )

    return prompt.strip()
