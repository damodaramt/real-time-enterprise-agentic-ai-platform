from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.mcp.models import (
    MCPToolRequest
)

from app.mcp.orchestrator import (
    execute_mcp_tool
)

router = APIRouter()


@router.post(
    "/mcp",
    status_code=status.HTTP_200_OK
)
def run_mcp_tool(
    request: MCPToolRequest
):

    try:

        result = execute_mcp_tool(
            tool_name=request.tool_name,
            query=request.query
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="MCP execution failed."
        )
