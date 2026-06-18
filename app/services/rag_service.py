import logging

from app.services.embedding_service import generate_query_embedding
from app.services.retrieval_service import search_documents
from app.services.context_builder import build_context
from app.services.prompt_builder import build_prompt
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

llm = LLMService()


async def ask_question(
    query: str,
) -> dict:

    logger.info("Received query: %s", query)

    embedding = generate_query_embedding(query)

    documents = search_documents(embedding)

    context = build_context(documents)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    answer = await llm.generate_answer(prompt)

    return {
        "query": query,
        "answer": answer,
        "context": context,
        "documents": documents,
    }
