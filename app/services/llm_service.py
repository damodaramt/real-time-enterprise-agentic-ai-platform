import logging

import requests

from app.core.config import settings


logger = logging.getLogger(__name__)


def generate_response(
    prompt: str
) -> str:

    """
    Generate LLM response
    using Ollama local inference.
    """

    try:

        response = requests.post(
            url=(
                f"{settings.OLLAMA_BASE_URL}"
                "/api/generate"
            ),
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        )

    except Exception as error:

        logger.exception(
            "LLM generation failed: %s",
            str(error)
        )

        raise
