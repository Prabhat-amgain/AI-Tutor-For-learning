import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_DIR = "data"
CHROMA_DIR = "data/chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_documents():
    """Load every .pdf and .txt file in data/ into LangChain Document objects."""
    docs = []
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if filename.lower().endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif filename.lower().endswith(".txt"):
            docs.extend(TextLoader(path, encoding="utf-8").load())
    return docs


def build_vectorstore():
    """Ingestion pipeline: load -> split into chunks -> embed -> persist to disk."""
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)  # start fresh so re-running doesn't duplicate old chunks

    raw_docs = load_documents()
    if not raw_docs:
        raise ValueError(f"No .pdf or .txt files found in {DATA_DIR}/. Add notes there first.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(raw_docs)

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=CHROMA_DIR
    )
    print(f"Ingested {len(raw_docs)} document(s) -> {len(chunks)} chunks -> saved to {CHROMA_DIR}")
    return vectorstore


if __name__ == "__main__":
    build_vectorstore()