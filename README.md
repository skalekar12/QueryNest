# 🧠 Query Nest — RAG-based Document Q&A System

Query Nest is a **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents (PDFs) and ask questions about them.
It combines **semantic search (FAISS)** with **LLMs (Gemini)** to provide accurate, context-aware answers.

---

## 🚀 Features

* 📄 Upload and process PDF documents
* ✂️ Intelligent text chunking
* 🔎 Semantic search using FAISS
* 🧠 Context-aware answers using Gemini API
* ⚡ Fast retrieval pipeline
* 🧩 Modular backend (clean architecture)

---

## 🏗️ Project Structure

```
QueryNest/
│
├── app/
│   ├── api/                # API routes
│   ├── core/               # Config & Gemini client
│   ├── models/             # Data schemas
│   ├── services/           # RAG pipeline components
│   │   ├── chunking.py
│   │   ├── embedding.py
│   │   ├── pdf_loader.py
│   │   ├── rag_pipeline.py
│   │   └── vector_store.py
│   ├── utils/              # Helper functions
│   └── main.py             # Entry point
│
├── data/
│   ├── raw/                # Input PDFs
│   ├── processed/          # Processed data
│   └── faiss/              # Saved FAISS index
│
├── index.html              # Frontend UI
├── make_files.py           # Setup script (optional)
├── requirements.txt        # Dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/query-nest
cd query-nest
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate it:

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔐 Environment Variables (.env)

Create a `.env` file in the root directory:

```
QUERYNEST/
├── .env   ← create this file
```

Add your API key:

```
GEMINI_API_KEY=your_api_key_here
```

💡 You can get your API key from Google AI Studio.

---

## ▶️ Running the Application

### Step 1: Start Backend

```
python app/main.py
```

---

### Step 2: Open Frontend

Open `index.html` in your browser.

---

## 📌 How It Works

1. Upload PDF → stored in `data/raw/`
2. Text is extracted using `pdf_loader.py`
3. Content is chunked via `chunking.py`
4. Embeddings generated using `embedding.py`
5. Stored in FAISS (`vector_store.py`)
6. Query → embedding → similarity search
7. Top chunks passed to Gemini → final answer

---

## 🧪 Example Workflow

* Upload: `bert.pdf`
* Ask: *"What is attention mechanism?"*
* System:

  * Retrieves relevant chunks
  * Sends context to Gemini
  * Returns precise answer

---

## 🧠 Tech Stack

* Python
* FAISS (Vector DB)
* Gemini API (LLM)
* HTML (Frontend)
* Custom RAG Pipeline

---

## 🛠️ Future Improvements

* 🌐 Deploy on cloud (Render / AWS)
* 📂 Multi-document querying
* 💬 Chat history memory
* 📊 Better UI (React)
* 🔐 Auth system

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## ⭐ Support

If you like this project, consider giving it a star ⭐

---
