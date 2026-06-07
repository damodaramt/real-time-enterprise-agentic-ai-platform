import logging

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self) -> None:

        if not settings.OPENAI_API_KEY:

            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=60.0
        )

    async def generate_answer(
        self,
        prompt: str
    ) -> str:

        if not prompt:

            raise ValueError(
                "Prompt cannot be empty."
            )

        prompt = prompt.strip()

        if not prompt:

            raise ValueError(
                "Prompt cannot be empty."
            )

        try:

            logger.info(
                "Generating LLM response. "
                "model=%s prompt_chars=%s",
                settings.OPENAI_MODEL,
                len(prompt)
            )

            response = (
                await self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    temperature=settings.OPENAI_TEMPERATURE,
                    max_tokens=settings.OPENAI_MAX_TOKENS,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            if not response.choices:

                raise RuntimeError(
                    "OpenAI returned no choices."
                )

            message = (
                response
                .choices[0]
                .message
            )

            if message is None:

                raise RuntimeError(
                    "OpenAI returned empty message."
                )

            answer = (
                message.content
            )

            if not answer:

                raise RuntimeError(
                    "OpenAI returned empty content."
                )

            logger.info(
                "LLM response generated successfully."
            )

            return answer.strip()

        except Exception as error:

            logger.exception(
                "LLM generation failed. "
                "model=%s error=%s",
                settings.OPENAI_MODEL,
                str(error)
            )

            raise
