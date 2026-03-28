import uuid
import re


def sentence_tokenize(text: str):
    """
    Better sentence splitting (handles edge cases better than simple regex)
    """
    # basic but improved sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def split_text_into_chunks(text: str, max_tokens: int = 120, overlap_sentences: int = 2):
    """
    Sentence-aware chunking:
    - groups full sentences
    - keeps semantic meaning intact
    - uses sentence overlap instead of character overlap
    """

    if not text:
        return []

    sentences = sentence_tokenize(text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        # skip noisy sentences
        if word_count < 5:
            continue

        # if adding sentence exceeds limit → finalize chunk
        if current_length + word_count > max_tokens:
            chunk_text = " ".join(current_chunk).strip()

            if is_valid_chunk(chunk_text):
                chunks.append(chunk_text)

            # 🔥 sentence-level overlap (much better than char overlap)
            current_chunk = current_chunk[-overlap_sentences:]
            current_length = sum(len(s.split()) for s in current_chunk)

        current_chunk.append(sentence)
        current_length += word_count

    # last chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk).strip()
        if is_valid_chunk(chunk_text):
            chunks.append(chunk_text)

    return chunks


def is_valid_chunk(chunk: str) -> bool:
    """
    Filters garbage chunks
    """

    if not chunk:
        return False

    if len(chunk) < 50:
        return False

    if len(chunk.split()) < 10:
        return False

    # remove tokenized garbage
    garbage_tokens = ["<pad>", "<unk>", "<EOS>"]
    if any(token in chunk for token in garbage_tokens):
        return False

    # too many symbols → noisy chunk
    non_alpha_ratio = sum(1 for c in chunk if not c.isalnum() and c != " ") / len(chunk)
    if non_alpha_ratio > 0.3:
        return False

    return True


def create_chunks_with_metadata(text: str, source: str = "unknown"):
    """
    Create structured chunks with metadata
    """

    raw_chunks = split_text_into_chunks(text)

    structured_chunks = []

    for idx, chunk in enumerate(raw_chunks):
        if not is_valid_chunk(chunk):
            continue

        structured_chunks.append({
            "id": str(uuid.uuid4()),
            "text": chunk,
            "source": source,
            "chunk_index": idx
        })

    return structured_chunks