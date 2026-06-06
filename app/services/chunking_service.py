import logging
from typing import List

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

logger = logging.getLogger(__name__)


DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    "",
                ],
            )
        )

        logger.info(
            "ChunkingService initialized "
            "chunk_size=%s overlap=%s",
            chunk_size,
            chunk_overlap,
        )

    def chunk_text(
        self,
        text: str,
    ) -> List[str]:

        if not text:

            logger.warning(
                "Empty text received for chunking"
            )

            return []

        chunks = self.splitter.split_text(
            text
        )

        logger.info(
            "Generated %s chunks",
            len(chunks),
        )

        return chunks
