import logging

from fastapi import FastAPI

from app.api.ask import (
    router as ask_router,
)
from app.api.mcp import (
    router as mcp_router,
)
from app.api.search import (
    router as search_router,
)
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enterprise Agentic AI Platform",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event() -> None:

    logger.info(
        "Starting Enterprise Agentic AI Platform"
    )

    logger.info(
        "OpenAI model=%s",
        settings.OPENAI_MODEL,
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:

    logger.info(
        "Stopping Enterprise Agentic AI Platform"
    )


app.include_router(
    search_router,
    tags=["Search"],
)

app.include_router(
    ask_router,
    tags=["RAG"],
)

app.include_router(
    mcp_router,
    tags=["MCP"],
)


@app.get("/health")
def health_check() -> dict[str, str]:

    return {
        "status": "healthy",
    }
