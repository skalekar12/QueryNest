import uuid


def split_text_into_chunks(text: str, chunk_size: int = 700, overlap: int = 150):
    """
    Split text into overlapping word-based chunks.

    Args:
        text (str): Cleaned input text
        chunk_size (int): Number of words per chunk
        overlap (int): Number of overlapping words

    Returns:
        List[str]: List of text chunks
    """
    if not text:
        return []

    words = text.replace("\n", " ").split()
    chunks = []

    start = 0
    total_words = len(words)

    while start < total_words:
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words).strip()

        if chunk_text:
            chunks.append(chunk_text)

        # Move start forward with overlap
        start += (chunk_size - overlap)

    return chunks


def create_chunks_with_metadata(text: str, source: str = "unknown"):
    """
    Create chunks with metadata for tracking and citations.

    Args:
        text (str): Cleaned input text
        source (str): Source file name

    Returns:
        List[dict]
    """
    raw_chunks = split_text_into_chunks(text)

    structured_chunks = []

    for idx, chunk in enumerate(raw_chunks):
        structured_chunks.append({
            "id": str(uuid.uuid4()),   # unique ID (better than 1,2,3)
            "text": chunk,
            "source": source,
            "chunk_index": idx
        })

    return structured_chunks