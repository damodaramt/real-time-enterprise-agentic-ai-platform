import logging

import requests


logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


REQUEST_TIMEOUT_SECONDS = 5


def call_mcp_tool(
    endpoint: str,
    payload: dict
):

    try:

        response = requests.post(
            endpoint,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS
        )

        response.raise_for_status()

        logger.info(
            "MCP tool call successful: %s",
            endpoint
        )

        return response.json()

    except requests.Timeout:

        logger.exception(
            "MCP tool timeout: %s",
            endpoint
        )

        raise

    except requests.RequestException:

        logger.exception(
            "MCP tool request failed: %s",
            endpoint
        )

        raise
