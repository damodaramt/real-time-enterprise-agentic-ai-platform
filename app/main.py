from fastapi import FastAPI

from app.api.search import (
    router as search_router
)

from app.api.ask import (
    router as ask_router
)

from app.api.mcp import (
    router as mcp_router
)

from app.core.config import settings


app = FastAPI(
    title="Enterprise Agentic AI Platform",
    version="1.0.0"
)


app.include_router(
    search_router,
    tags=["Search"]
)

app.include_router(
    ask_router,
    tags=["RAG"]
)

app.include_router(
    mcp_router,
    tags=["MCP"]
)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL
    }
