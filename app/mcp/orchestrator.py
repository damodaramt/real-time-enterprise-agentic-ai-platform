from app.mcp.client import (
    call_mcp_tool
)

from app.mcp.registry import (
    MCP_TOOLS
)


def execute_mcp_tool(
    tool_name: str,
    query: str
):

    tool = MCP_TOOLS.get(
        tool_name
    )

    if not tool:

        raise ValueError(
            f"Unknown MCP tool: {tool_name}"
        )

    return call_mcp_tool(
        endpoint=tool["endpoint"],
        payload={
            "query": query
        }
    )
