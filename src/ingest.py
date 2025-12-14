import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
VECTOR_DIR = os.getenv("VECTOR_DIR", "vectors")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))


def load_documents(data_dir: Path) -> List:
    """Load all .txt files from the data directory."""
    docs = []
    for path in sorted(data_dir.rglob("*.txt")):
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    if not docs:
        raise SystemExit(f"No documents found under {data_dir}")
    return docs


def make_splitter(chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """Create the text splitter used for chunking documents."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
    )


def ingest():
    docs = load_documents(DATA_DIR)
    splitter = make_splitter()
    chunks = splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    store = FAISS.from_documents(chunks, embeddings)
    Path(VECTOR_DIR).mkdir(parents=True, exist_ok=True)
    store.save_local(VECTOR_DIR)
    print(
        f"Ingested {len(chunks)} chunks from {len(docs)} documents "
        f"into {VECTOR_DIR}"
    )


if __name__ == "__main__":
    ingest()
