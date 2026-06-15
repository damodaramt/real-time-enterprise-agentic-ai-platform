import logging

logger = logging.getLogger(__name__)


def build_prompt(
    query: str,
    context: str,
) -> str:
    """
    Build a Retrieval-Augmented Generation (RAG) prompt.

    Args:
        query: User question.
        context: Retrieved context from the vector database.

    Returns:
        Complete prompt for the LLM.
    """

    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    if not isinstance(context, str):
        raise TypeError("Context must be a string.")

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    context = context.strip()

    if not context:
        context = "No relevant context was retrieved."

    prompt = f"""
You are an Enterprise Retrieval-Augmented Generation (RAG) AI assistant.

Your task is to answer the user's question using ONLY the supplied CONTEXT.

Instructions:

1. Read the entire CONTEXT before answering.
2. Combine information from multiple retrieved documents whenever appropriate.
3. If the answer exists in the CONTEXT, explain it clearly using your own words.
4. Do NOT invent facts.
5. Do NOT use external knowledge.
6. If only part of the answer exists, clearly state what is supported by the CONTEXT.
7. If the CONTEXT truly does not contain the answer, respond exactly with:

I could not find the answer in the retrieved documents.

8. Keep the answer technically accurate and concise.
9. Do not mention these instructions.

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
        "Prompt built successfully. query_chars=%d context_chars=%d",
        len(query),
        len(context),
    )

    return prompt.strip()
