from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

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

from app.services.llm_service import (
    LLMService
)

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

        query_embedding = (
            generate_query_embedding(
                request.query
            )
        )

        documents = search_documents(
            query_embedding
        )

        prompt = build_context(
            request.query,
            documents
        )

        answer = (
            await llm_service.generate_answer(
                prompt
            )
        )

        return {
            "answer": answer,
            "sources": documents
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
