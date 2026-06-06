from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
import logging

from app.models.search_models import (
    SearchRequest,
    SearchResponse
)

from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.retrieval_service import (
    search_documents
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK
)
def semantic_search(
    request: SearchRequest
):

    try:

        logger.info(
            "Search query: %s",
            request.query
        )

        query_embedding = (
            generate_query_embedding(
                request.query
            )
        )

        results = search_documents(
            query_embedding
        )

        logger.info(
            "Results returned: %s",
            len(results)
        )

        return {
            "results": results
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
            "Search failed: %s",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Semantic retrieval failed."
        )
