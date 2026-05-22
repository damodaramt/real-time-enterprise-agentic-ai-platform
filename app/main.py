from fastapi import FastAPI

from app.api.search import (
    router as search_router
)

from app.api.mcp import (
    router as mcp_router
)

app = FastAPI(
    title="Enterprise Agentic AI Platform",
    version="1.0.0"
)

app.include_router(
    search_router
)

app.include_router(
    mcp_router
)


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
