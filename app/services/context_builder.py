import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Set

logger = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 6000


def build_context(
    retrieved_documents: List[Dict[str, Any]]
) -> str:

    if not isinstance(
        retrieved_documents,
        list
    ):
        raise TypeError(
            "retrieved_documents must be a list."
        )

    if not retrieved_documents:

        logger.warning(
            "No retrieved documents found."
        )

        return ""

    context_parts: List[str] = []

    seen_chunks: Set[str] = set()

    total_chars = 0

    sorted_docs = sorted(
        retrieved_documents,
        key=lambda x: x.get(
            "distance",
            999.0
        )
    )

    for index, doc in enumerate(
        sorted_docs,
        start=1
    ):

        if not isinstance(
            doc,
            dict
        ):
            continue

        content = (
            str(
                doc.get(
                    "content",
                    ""
                )
            )
            .strip()
        )

        if not content:
            continue

        if content in seen_chunks:
            continue

        seen_chunks.add(
            content
        )

        metadata = doc.get(
            "metadata"
        )

        if not isinstance(
            metadata,
            dict
        ):
            metadata = {}

        source = metadata.get(
            "source",
            "unknown"
        )

        try:

            distance = round(
                float(
                    doc.get(
                        "distance",
                        0.0
                    )
                ),
                4
            )

        except (
            TypeError,
            ValueError,
        ):

            distance = 0.0

        chunk = (
            f"[DOCUMENT {index}]\n"
            f"Source: {source}\n"
            f"Distance: {distance}\n\n"
            f"{content}\n"
        )

        chunk_size = len(
            chunk
        )

        if (
            total_chars + chunk_size
            > MAX_CONTEXT_CHARS
        ):

            logger.info(
                "Context size limit reached."
            )

            break

        context_parts.append(
            chunk
        )

        total_chars += chunk_size

    context = "\n".join(
        context_parts
    )

    logger.info(
        "Context built successfully. chars=%s docs=%s",
        total_chars,
        len(context_parts),
    )

    return context
