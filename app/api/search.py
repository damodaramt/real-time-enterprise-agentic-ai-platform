from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

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

        query_embedding = (
            generate_query_embedding(
                request.query
            )
        )

        results = search_documents(
            query_embedding
        )

        return {
            "results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Semantic retrieval failed."
        )
