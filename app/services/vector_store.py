import faiss
import numpy as np
import pickle
import os


def create_faiss_index(embeddings: np.ndarray):
    """
    Create FAISS index and add embeddings.

    Args:
        embeddings (np.ndarray): shape (num_chunks, dim)

    Returns:
        faiss.Index
    """
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings)

    embeddings = embeddings.astype("float32")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index


def save_faiss_index(index, path: str):
    """
    Save FAISS index to disk.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)


def load_faiss_index(path: str):
    """
    Load FAISS index from disk.
    """
    return faiss.read_index(path)


def save_metadata(chunks, path: str):
    """
    Save chunk metadata (text + info).
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(chunks, f)


def load_metadata(path: str):
    """
    Load chunk metadata.
    """
    with open(path, "rb") as f:
        return pickle.load(f)


def search_index(index, query_vector: np.ndarray, k: int = 5):
    """
    Search FAISS index.

    Args:
        index: FAISS index
        query_vector (np.ndarray): shape (dim,)
        k (int): number of results

    Returns:
        distances, indices
    """
    if query_vector.ndim == 1:
        query_vector = np.expand_dims(query_vector, axis=0)

    query_vector = query_vector.astype("float32")

    distances, indices = index.search(query_vector, k)

    return distances[0], indices[0]