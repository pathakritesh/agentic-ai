import chromadb
from fastapi import FastAPI
from pydantic import BaseModel

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# ---------------- CONFIG ----------------

PDF_DIR = "./data/pdfs"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "pdf_rag"

# ---------------- FASTAPI ----------------

app = FastAPI(title="Local PDF RAG with Citations")

# ---------------- MODELS ----------------

embed_model = OllamaEmbedding(model_name="nomic-embed-text")

llm = Ollama(
    model="llama3.2:3b",
    temperature=0,
    request_timeout=120,
    additional_kwargs={"num_ctx": 2048}
)

Settings.embed_model = embed_model
Settings.llm = llm

# ---------------- VECTOR STORE ----------------

chroma_client = chromadb.Client(
    settings=chromadb.Settings(persist_directory=CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

vector_store = ChromaVectorStore(chroma_collection=collection)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# ---------------- INDEX ----------------

if collection.count() == 0:
    documents = SimpleDirectoryReader(PDF_DIR).load_data()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )
else:
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )

query_engine = index.as_query_engine(
    similarity_top_k=1,
    response_mode="compact"
)

# ---------------- API SCHEMA ----------------

class Question(BaseModel):
    question: str

# ---------------- ENDPOINT ----------------

@app.post("/ask")
def ask_pdf(q: Question):
    response = query_engine.query(q.question)

    # Deduplicate (file, page)
    unique_sources = {
        (node.metadata.get("file_name"), node.metadata.get("page_label"))
        for node in response.source_nodes
    }

    sources = [
        {"file_name": f, "page": p}
        for f, p in unique_sources
        if f and p
    ]

    return {
        "answer": response.response,
        "sources": sources
    }
