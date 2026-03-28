from pathlib import Path

# Folder structure
dirs = [
    "app/api",
    "app/core",
    "app/services",
    "app/models",
    "app/utils",
    "data/raw",
    "data/processed",
    "faiss_index",
]

# Files to create
files = [
    "app/main.py",
    "app/api/routes.py",
    "app/core/config.py",
    "app/core/gemini_client.py",
    "app/services/pdf_loader.py",
    "app/services/chunking.py",
    "app/services/embedding.py",
    "app/services/vector_store.py",
    "app/services/rag_pipeline.py",
    "app/models/schema.py",
    "app/utils/helpers.py",
    ".env",
    "requirements.txt",
    "README.md",
]

# Create directories
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

# Create files
for f in files:
    path = Path(f)
    path.touch(exist_ok=True)

print("✅ Project structure created successfully!")