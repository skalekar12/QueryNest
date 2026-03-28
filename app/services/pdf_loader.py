import fitz  # PyMuPDF
import re


def load_pdf(file_path: str):
    """
    Load PDF and extract text using block-based layout (FIXED).
    """
    doc = fitz.open(file_path)

    pages_data = []
    full_text_parts = []

    for page_number, page in enumerate(doc, start=1):

        blocks = page.get_text("blocks")  # 🔥 KEY CHANGE

        # Sort blocks top-to-bottom, left-to-right
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

        page_text_parts = []

        for block in blocks:
            text = block[4].strip()

            if not text:
                continue

            page_text_parts.append(text)

        page_text = " ".join(page_text_parts)

        if not page_text.strip():
            continue

        pages_data.append({
            "page": page_number,
            "text": page_text
        })

        full_text_parts.append(page_text)

    doc.close()

    full_text = "\n\n".join(full_text_parts)

    return {
        "full_text": full_text,
        "pages": pages_data
    }


# 🔥 MAIN CLEANING FUNCTION (UPGRADED)
def clean_text(text: str) -> str:
    """
    Clean text for high-quality RAG.

    Fixes:
    - broken words
    - hyphen splits
    - extra spaces
    - noisy formatting
    """

    if not text:
        return ""

    # 🔹 Replace newlines with space (important BEFORE word fixes)
    text = text.replace("\n", " ")

    # 🔹 Fix broken words like "mul ti" → "multi"
    text = re.sub(r'(\w)\s+(\w)', r'\1 \2', text)

    # 🔹 Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # 🔹 Remove references like [1], [23]
    text = re.sub(r'\[\d+\]', '', text)

    # 🔹 Remove figure/table mentions
    text = re.sub(r'(Figure|Table)\s*\d+.*?(?=\.)', '', text)

    # 🔹 Remove weird math artifacts (optional but useful)
    text = re.sub(r'√\w+', '', text)

    # 🔹 Strip
    text = text.strip()

    return text


# 🔥 EXTRA NOISE REMOVAL (OPTIONAL BUT STRONG)
def remove_noise(text: str) -> str:
    """
    Removes academic PDF noise.
    """

    # Remove citation-heavy lines
    text = re.sub(r'\b(et al\.?)', '', text)

    # Remove excessive numbers (like tables)
    text = re.sub(r'\b\d+\.\d+\b', '', text)

    return text.strip()


def extract_text_from_pdf(file_path: str):
    """
    Main ingestion function for RAG.
    """

    data = load_pdf(file_path)

    # 🔥 Clean full text
    cleaned_full_text = clean_text(data["full_text"])
    cleaned_full_text = remove_noise(cleaned_full_text)

    # 🔥 Clean pages individually (important for citations later)
    cleaned_pages = [
        {
            "page": page["page"],
            "text": remove_noise(clean_text(page["text"]))
        }
        for page in data["pages"]
    ]

    return {
        "full_text": cleaned_full_text,
        "pages": cleaned_pages,
        "num_pages": len(cleaned_pages)
    }