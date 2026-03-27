import fitz  # PyMuPDF
import re


def load_pdf(file_path: str):
    """
    Load a PDF and extract texts page by page.

    Returns:
        dict:
            {
                "full_text": str,
                "pages": [{"page": int, "text": str}]
            }
    """
    doc = fitz.open(file_path)

    pages_data = []
    full_text_parts = []

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()

        # Skip empty or whitespace-only pages
        if not text or not text.strip():
            continue

        text = text.strip()

        pages_data.append({
            "page": page_number,
            "text": text
        })

        # Add spacing between pages
        full_text_parts.append(text)

    doc.close()

    full_text = "\n\n".join(full_text_parts)

    return {
        "full_text": full_text,
        "pages": pages_data
    }


def clean_text(text: str) -> str:
    """
    Clean extracted text for embedding.

    - Normalize spaces
    - Remove excessive newlines
    - Keep punctuation (important for RAG)
    """
    if not text:
        return ""

    # Replace multiple newlines with max two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Fix spacing around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def extract_text_from_pdf(file_path: str):
    """
    Wrapper function for PDF ingestion.

    This is the ONLY function your API should call.
    """
    data = load_pdf(file_path)

    cleaned_full_text = clean_text(data["full_text"])

    # Clean each page individually (important for future citations)
    cleaned_pages = [
        {
            "page": page["page"],
            "text": clean_text(page["text"])
        }
        for page in data["pages"]
    ]

    return {
        "full_text": cleaned_full_text,
        "pages": cleaned_pages,
        "num_pages": len(cleaned_pages)
    }