from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class SearchRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )


class SearchResult(BaseModel):

    id: str

    content: str

    metadata: Dict[str, Any]

    distance: float


class SearchResponse(BaseModel):

    results: List[SearchResult]
