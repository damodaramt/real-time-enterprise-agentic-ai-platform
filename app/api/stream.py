import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import StreamingResponse

from app.models.search_models import SearchRequest

from app.services.embedding_service import (
    generate_query_embedding,
)

from app.services.retrieval_service import (
    search_documents,
)

from app.services.context_builder import (
    build_context,
)

from app.services.prompt_builder import (
    build_prompt,
)

from app.services.llm_service import (
    LLMService,
)

logger = logging.getLogger(__name__)

router = APIRouter()

llm_service = LLMService()


@router.post(
    "/stream",
    status_code=status.HTTP_200_OK,
)
async def stream_answer(
    request: SearchRequest,
):

    try:

        logger.info(
            "Streaming question received: %s",
            request.query,
        )

        query_embedding = generate_query_embedding(
            request.query
        )

        documents = search_documents(
            query_embedding
        )

        logger.info(
            "Retrieved documents=%s",
            len(documents),
        )

        context = build_context(
            documents
        )

        prompt = build_prompt(
            query=request.query,
            context=context,
        )

        async def event_generator():

            async for token in llm_service.stream_answer(
                prompt
            ):
                yield token

        return StreamingResponse(
            event_generator(),
            media_type="text/plain",
        )

    except ValueError as error:

        logger.exception(
            "Validation error: %s",
            str(error),
        )

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        logger.exception(
            "Streaming pipeline failed: %s",
            str(error),
        )

        raise HTTPException(
            status_code=500,
            detail="Streaming failed.",
        )
