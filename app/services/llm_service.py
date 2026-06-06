import logging

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    async def generate_answer(
        self,
        prompt: str
    ) -> str:

        try:

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

            answer = (
                response
                .choices[0]
                .message
                .content
            )

            return answer.strip()

        except Exception as error:

            logger.exception(
                "LLM generation failed: %s",
                str(error)
            )

            raise
