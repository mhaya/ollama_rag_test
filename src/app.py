import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from pydantic import BaseModel

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
VECTOR_DIR = os.getenv("VECTOR_DIR", "vectors")
DEFAULT_TOP_K = int(os.getenv("TOP_K", "4"))
TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a concise, helpful assistant. Ground responses in the provided context.",
)

embeddings = OllamaEmbeddings(model=EMBED_MODEL)
llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE)
vector_store = None


def get_vector_store():
    """Lazy-load the FAISS index; instruct user to ingest if missing."""
    global vector_store
    if vector_store is None:
        if not Path(VECTOR_DIR).exists():
            raise HTTPException(
                status_code=500,
                detail=f"Vector store not found at {VECTOR_DIR}. Run `make ingest` first.",
            )
        vector_store = FAISS.load_local(
            VECTOR_DIR, embeddings, allow_dangerous_deserialization=True
        )
    return vector_store

app = FastAPI(title="Ollama RAG Chat")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatPayload(BaseModel):
    message: str
    top_k: int | None = None


def build_prompt(context: str, question: str) -> str:
    """Build the prompt used for RAG responses."""
    context_block = context.strip() or "No context retrieved."
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context_block}\n\n"
        f"User: {question}\n"
        f"Assistant:"
    )


def format_context(docs) -> str:
    """Format retrieved documents into a readable context block."""
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        formatted.append(f"[{source}] {doc.page_content}")
    return "\n\n".join(formatted)


def stream_answer(prompt: str) -> Iterable[str]:
    """Stream tokens from the LLM back to the caller."""
    for chunk in llm.stream(prompt):
        yield chunk.content


@app.post("/chat")
async def chat(payload: ChatPayload):
    k = payload.top_k or DEFAULT_TOP_K
    store = get_vector_store()
    docs = store.similarity_search(payload.message, k=k)
    context_block = format_context(docs)
    prompt = build_prompt(context_block, payload.message)
    return StreamingResponse(stream_answer(prompt), media_type="text/plain")


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME, "embed_model": EMBED_MODEL}
