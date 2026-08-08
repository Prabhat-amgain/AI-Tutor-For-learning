from app.rag.ingest import build_vectorstore
from app.rag.retriever import retrieve_relevant_chunks

build_vectorstore()  # run ingestion once

print("=== Query 1: never says 'hash table' ===")
print(retrieve_relevant_chunks("What data structure gives constant time lookups on average?"))

print("\n=== Query 2: never says 'binary search tree' ===")
print(retrieve_relevant_chunks("How does an unbalanced tree affect search performance?"))