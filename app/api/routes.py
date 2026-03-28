import os
import shutil
import traceback
from flask import Blueprint, request, jsonify
from app.services.pdf_loader import load_pdf, extract_text_from_pdf
from app.services.chunking import create_chunks_with_metadata
from app.services.embedding import generate_embeddings
from app.services.vector_store import (
    create_faiss_index,
    save_faiss_index,
    save_metadata,
    load_faiss_index,
    load_metadata
)
from app.services.rag_pipeline import run_rag_pipeline

router = Blueprint("router", __name__)

DATA_PATH = "data"
RAW_PATH = os.path.join(DATA_PATH, "raw")
INDEX_PATH = os.path.join(DATA_PATH, "faiss")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(INDEX_PATH, exist_ok=True)


@router.post("/upload")
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        file_path = os.path.join(RAW_PATH, file.filename)
        file.save(file_path)

        result = extract_text_from_pdf(file_path)
        full_text = result["full_text"]

        if not full_text or not full_text.strip():
            return jsonify({"error": "Empty or invalid PDF"}), 400

        chunks = create_chunks_with_metadata(full_text, source=file.filename)
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = generate_embeddings(chunk_texts)
        index = create_faiss_index(embeddings)

        index_file = os.path.join(INDEX_PATH, "index.faiss")
        metadata_file = os.path.join(INDEX_PATH, "metadata.pkl")

        save_faiss_index(index, index_file)
        save_metadata(chunks, metadata_file)

        return jsonify({
            "message": "PDF processed successfully",
            "num_chunks": len(chunks),
            "num_pages": result["num_pages"]
        }), 200

    except Exception as e:
        return jsonify({"error": traceback.format_exc()}), 500


@router.post("/ask")
def ask_question():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        index_file = os.path.join(INDEX_PATH, "index.faiss")
        metadata_file = os.path.join(INDEX_PATH, "metadata.pkl")

        if not os.path.exists(index_file):
            return jsonify({"error": "No index found. Upload a PDF first."}), 400

        from app.services.embedding import embed_query  # ← import embed function

        index = load_faiss_index(index_file)
        metadata = load_metadata(metadata_file)

        answer = run_rag_pipeline(
            query=data["question"],
            index=index,
            metadata=metadata,          # ← was chunks
            embed_query_fn=embed_query  # ← was missing
        )

        return jsonify(answer), 200

    except Exception as e:
        return jsonify({"error": traceback.format_exc()}), 500