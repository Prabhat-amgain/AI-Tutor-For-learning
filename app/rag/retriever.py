from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.rag.ingest import CHROMA_DIR

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def retrieve_relevant_chunks(query: str, k: int = 3) -> str:
    """Find the k most semantically relevant chunks from the student's notes."""
    results = _vectorstore.similarity_search(query, k=k)
    if not results:
        return "No relevant material found in the student's notes."
    return "\n\n---\n\n".join(doc.page_content for doc in results)