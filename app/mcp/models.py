from pydantic import BaseModel
from pydantic import Field


class MCPToolRequest(BaseModel):

    tool_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )
