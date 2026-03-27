import uuid

import re


def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Smarter chunking using sentence boundaries + overlap
    """

    if not text:
        return []

    # 🧠 Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text.replace("\n", " "))

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding sentence stays within limit
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())

            # 🔥 overlap: keep last part
            overlap_text = current_chunk[-overlap:]
            current_chunk = overlap_text + " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

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