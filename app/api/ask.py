from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

import logging

from app.models.search_models import SearchRequest

from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.retrieval_service import (
    search_documents
)

from app.services.context_builder import (
    build_context
)

from app.services.prompt_builder import (
    build_prompt
)

from app.services.llm_service import (
    LLMService
)

logger = logging.getLogger(__name__)

router = APIRouter()

llm_service = LLMService()


@router.post(
    "/ask",
    status_code=status.HTTP_200_OK
)
async def ask_question(
    request: SearchRequest
):

    try:

        logger.info(
            "Question received: %s",
            request.query
        )

        query_embedding = (
            generate_query_embedding(
                request.query
            )
        )

        documents = search_documents(
            query_embedding
        )

        logger.info(
            "Retrieved documents=%s",
            len(documents)
        )

        context = build_context(
            documents
        )

        prompt = build_prompt(
            query=request.query,
            context=context
        )

        answer = (
            await llm_service.generate_answer(
                prompt
            )
        )

        logger.info(
            "Answer generated successfully."
        )

        return {
            "answer": answer,
            "sources": documents
        }

    except ValueError as error:

        logger.exception(
            "Validation error: %s",
            str(error)
        )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        logger.exception(
            "RAG pipeline failed: %s",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Answer generation failed."
        )
