import numpy as np


def retrieve_relevant_chunks(
    query,
    index,
    metadata,
    embed_query_fn,
    k=5,
    search_k=10
):
    """
    Retrieve top-k diverse, relevant chunks from FAISS

    Args:
        query (str): user query
        index: FAISS index
        metadata (list): chunk data (dict or string)
        embed_query_fn: function to embed query
        k (int): final number of chunks
        search_k (int): initial search pool (must be > k)

    Returns:
        List[str]: filtered relevant chunks
    """

    print("👉 Embedding query...")

    # 🔹 Step 1: format query
    query = query.strip()
    formatted_query = f"query: {query}"

    # 🔹 Step 2: embed
    query_vector = embed_query_fn(formatted_query)
    query_vector = np.array([query_vector]).astype("float32")

    print("✅ Query embedded")

    # 🔹 Step 3: FAISS search
    print("👉 Searching FAISS...")
    distances, indices = index.search(query_vector, search_k)
    print("✅ FAISS search done")

    print("\nRAW INDICES:", indices[0])

    # 🔹 Step 4: collect raw results
    raw_chunks = []
    raw_distances = []

    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            chunk = metadata[idx]

            # handle dict or string
            if isinstance(chunk, dict):
                text = chunk.get("text", "")
            else:
                text = chunk

            raw_chunks.append(text)
            raw_distances.append(distances[0][i])

    # 🔍 DEBUG
    print("\n🔍 Raw Retrieval:")
    for i, (chunk, dist) in enumerate(zip(raw_chunks, raw_distances)):
        print(f"\nRank {i+1} | Distance: {dist:.4f}")
        print(chunk[:150])

    # 🔹 Step 5: deduplicate (exact + near)
    def is_similar(a, b, threshold=0.9):
        # simple fast similarity check
        return a[:200] == b[:200]

    unique_chunks = []

    for chunk in raw_chunks:
        clean_chunk = chunk.strip()

        # skip empty
        if not clean_chunk:
            continue

        # check similarity
        if not any(is_similar(clean_chunk, existing) for existing in unique_chunks):
            unique_chunks.append(clean_chunk)

        if len(unique_chunks) >= k:
            break

    print("\n✅ After Deduplication:")
    for i, chunk in enumerate(unique_chunks):
        print(f"\nFinal {i+1}:")
        print(chunk[:150])

    return unique_chunks


def format_context(chunks):
    """
    Format chunks into structured context for LLM
    """

    if not chunks:
        return "No relevant context found."

    context = "Context:\n\n"

    for i, chunk in enumerate(chunks):
        context += f"{i+1}. {chunk}\n\n"

    return context
from app.core.gemini_client import generate_response


def run_rag_pipeline(query, index, metadata, embed_query_fn, k=5):
    """
    Full RAG pipeline:
    query → retrieval → context → LLM → answer
    """

    print("\n🚀 Running full RAG pipeline...\n")

    # 🔹 Step 1: Retrieve chunks
    chunks = retrieve_relevant_chunks(
        query=query,
        index=index,
        metadata=metadata,
        embed_query_fn=embed_query_fn,
        k=k,
        search_k=10
    )

    # 🔹 Step 2: Format context
    context = format_context(chunks)

    print("\n🧠 Sending to Gemini...\n")

    # 🔹 Step 3: Generate answer
    answer = generate_response(query, context)

    return answer