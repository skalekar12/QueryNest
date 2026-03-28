import numpy as np
from app.core.gemini_client import generate_response


# 🔹 RETRIEVAL FUNCTION
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
    """

    print("👉 Embedding query...")

    # Format query
    query = query.strip()
    formatted_query = f"query: {query}"

    # Embed
    query_vector = embed_query_fn(formatted_query)
    query_vector = np.array([query_vector]).astype("float32")

    print("✅ Query embedded")

    # FAISS search
    print("👉 Searching FAISS...")
    distances, indices = index.search(query_vector, search_k)
    print("✅ FAISS search done")

    print("\nRAW INDICES:", indices[0])

    # Collect raw results
    raw_chunks = []
    raw_distances = []

    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            chunk = metadata[idx]

            if isinstance(chunk, dict):
                text = chunk.get("text", "")
            else:
                text = chunk

            raw_chunks.append(text)
            raw_distances.append(distances[0][i])

    # DEBUG
    print("\n🔍 Raw Retrieval:")
    for i, (chunk, dist) in enumerate(zip(raw_chunks, raw_distances)):
        print(f"\nRank {i+1} | Distance: {dist:.4f}")
        print(chunk[:150])

    # Deduplicate
    def is_similar(a, b):
        return a[:200] == b[:200]

    unique_chunks = []

    for chunk in raw_chunks:
        clean_chunk = chunk.strip()

        if not clean_chunk:
            continue

        if not any(is_similar(clean_chunk, existing) for existing in unique_chunks):
            unique_chunks.append(clean_chunk)

        if len(unique_chunks) >= k:
            break

    print("\n✅ After Deduplication:")
    for i, chunk in enumerate(unique_chunks):
        print(f"\nFinal {i+1}:")
        print(chunk[:150])

    return unique_chunks


# 🔹 CONTEXT FORMATTER (UPDATED)
def format_context(chunks):
    """
    Clean context formatting for LLM
    """

    if not chunks:
        return "No relevant context found."

    # 🔥 Clean format (no numbering = better LLM output)
    return "\n\n".join(chunks)


# 🔹 MAIN RAG PIPELINE (UPDATED)
def run_rag_pipeline(query, index, metadata, embed_query_fn, k=5):
    """
    Full RAG pipeline:
    query → retrieval → context → LLM → answer
    """

    print("\n🚀 Running full RAG pipeline...\n")

    # 1. Retrieve chunks
    chunks = retrieve_relevant_chunks(
        query=query,
        index=index,
        metadata=metadata,
        embed_query_fn=embed_query_fn,
        k=k,
        search_k=10
    )

    # 2. Format context
    context = format_context(chunks)

    print("\n🧠 Sending to Gemini...\n")

    # 🔥 3. STRONG PROMPT (MAIN IMPROVEMENT)
    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the question.

Explain the answer in simple, easy-to-understand language.
Avoid technical jargon unless necessary.
If helpful, use examples or analogies.

If the answer is not present in the context, say:
"I don't know based on the document.
Do not make up information. Only use the context.
Ignore irrelevant or noisy context."

Context:
{context}

Question:
{query}

Answer:
"""

    # 4. Generate answer
    answer = generate_response(prompt)

    # 🔥 OPTIONAL: return sources (NotebookLM style)
    return {
        "answer": answer,
        "sources": chunks[:3]
    }