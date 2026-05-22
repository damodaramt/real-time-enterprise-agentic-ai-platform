from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(
    file_path: str
) -> str:

    pdf_reader = PdfReader(
        file_path
    )

    text_chunks = []

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:

            text_chunks.append(
                page_text
            )

    return "\n".join(
        text_chunks
    )
