# 📄 Local RAG Agent (Ollama + LlamaIndex + Chroma)

A **fully local Retrieval-Augmented Generation (RAG) system** that allows you to **chat with multiple PDF files** using **Ollama**, **LlamaIndex**, **ChromaDB**, **FastAPI**, and **Streamlit**.

This project is optimized to run on a **Windows laptop with 8 GB RAM**, without any external API keys (no OpenAI, no cloud dependency).

---

## ✨ Features

- 📚 Multi-PDF ingestion
- 🔎 Semantic search using vector embeddings
- 💬 Conversational chat interface
- 🧠 Local LLM inference via Ollama
- 💾 Persistent vector storage (ChromaDB)
- 📌 Source citations (PDF file name + page number)
- 🚀 FastAPI backend + Streamlit UI
- 🔒 Fully offline & privacy-friendly

---

## 🧱 Architecture Overview

PDF Files
↓
LlamaIndex (Loader + Chunking)
↓
Ollama Embeddings (nomic-embed-text)
↓
ChromaDB (Persistent Vector Store)
↓
FastAPI (Query API)
↓
Streamlit (Chat UI)
↓
Ollama LLM (llama3.2:3b)


---

## 📁 Repository Structure

Local-RAG-Agent-V2/
│
├── Local-RAG-Agent-V2.ipynb # Jupyter notebook (experimentation)
├── app.py # FastAPI backend
├── streamlit_app.py # Streamlit chat UI
├── pyproject.toml # Dependencies
├── chroma_db/ # Persistent vector database
└── data/
└── pdfs/ # All PDF files go here


---

## ⚙️ Prerequisites

### 1️⃣ System Requirements
- OS: Windows / Linux / macOS
- RAM: **8 GB minimum**
- Python: **3.10+**
- Disk: ~5 GB free

---

3️⃣ Pull Required Models
ollama pull nomic-embed-text
ollama pull llama3.2:3b


Start Ollama:

ollama serve

🐍 Python Environment Setup
Create & activate virtual environment (Windows)
python -m venv .venv
.\.venv\Scripts\activate

Install dependencies
pip install -r requirements.txt


If using pyproject.toml:

pip install .

📄 Add PDF Files

Place all PDFs inside:

data/pdfs/


You can add 20+ PDFs for testing.

🚀 Running the Application
1️⃣ Start FastAPI Backend
uvicorn app:app --host 127.0.0.1 --port 8000 --reload


Verify backend is running:

Open: http://127.0.0.1:8000/docs

2️⃣ Start Streamlit UI (New Terminal)
streamlit run streamlit_app.py


Streamlit will open automatically in your browser.

💬 Usage

Type a question in the chat input

The system:

Searches relevant PDF chunks

Generates an answer using local LLM

Displays citations (PDF name + page number)

Example questions:

“Summarize the document”

“Which PDF talks about cost optimization?”

“Explain Kubernetes networking”

📌 Example API Response
{
  "answer": "The document explains cloud architecture best practices...",
  "sources": [
    {
      "file_name": "01_AWS_Architecture_Best_Practices.pdf",
      "page": "2"
    }
  ]
}

🧪 Jupyter Notebook

Local-RAG-Agent-V2.ipynb is included for:

Experimentation

Debugging

Learning LlamaIndex internals

⚠️ Production usage should rely on FastAPI + Streamlit, not the notebook.

🧠 Performance Notes (8 GB RAM)

Uses llama3.2:3b (small, stable model)

Context limited to 2048 tokens

Retrieval limited to top-1 chunk

Response mode set to compact

This avoids memory crashes on low-RAM systems.

🛠️ Troubleshooting
❌ Streamlit Connection Error
Connection refused (127.0.0.1:8000)


✅ Fix:

Ensure FastAPI is running

Check http://127.0.0.1:8000/docs

Start FastAPI before Streamlit

Ensure same virtual environment is used
