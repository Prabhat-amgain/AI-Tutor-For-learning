from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.rag.ingest import CHROMA_DIR

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

_vectorstore = None  # only opens the DB on first real search, not on import


def _get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return _vectorstore


def retrieve_relevant_chunks(query: str, k: int = 3) -> str:
    results = _get_vectorstore().similarity_search(query, k=k)
    if not results:
        return "No relevant material found in the student's notes."
    return "\n\n---\n\n".join(doc.page_content for doc in results)