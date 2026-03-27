from sentence_transformers import SentenceTransformer
import numpy as np

# Global model (loaded once)
_model = None


def load_embedding_model():
    """
    Load embedding model once and reuse.
    """
    global _model

    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en")

    return _model


def generate_embeddings(chunks, batch_size: int = 32):
    """
    Generate embeddings for document chunks.

    Args:
        chunks (List[str]): List of chunk texts
        batch_size (int): Batch size for encoding

    Returns:
        np.ndarray: Shape (num_chunks, embedding_dim)
    """
    model = load_embedding_model()

    # Add BGE passage prefix
    prefixed_chunks = [f"passage: {chunk}" for chunk in chunks]

    embeddings = model.encode(
        prefixed_chunks,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # IMPORTANT for cosine similarity
    )

    return embeddings


def embed_query(query: str):
    """
    Generate embedding for user query.

    Args:
        query (str)

    Returns:
        np.ndarray: Shape (embedding_dim,)
    """
    model = load_embedding_model()

    # BGE query prefix
    prefixed_query = f"query: {query}"

    embedding = model.encode(
        prefixed_query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding