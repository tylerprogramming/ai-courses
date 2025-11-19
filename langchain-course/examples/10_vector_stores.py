"""
Topic 10: Vector Stores and Embeddings

Vector stores enable semantic search by storing and querying embeddings.
Essential for RAG (Retrieval Augmented Generation).

Embeddings = numerical representations of text that capture meaning
Similar texts have similar embeddings

FAISS: Fast, local, in-memory (good for prototyping)
Chroma: Persistent, local (good for small-medium projects)
Pinecone: Cloud, managed (good for production/scale)
Weaviate: Cloud or self-hosted (enterprise)
Qdrant: Cloud or self-hosted (high performance)

LangChain provides same API across all stores - easy to swap!
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# Alternatives: Chroma (persistent), Pinecone (cloud), Weaviate, Qdrant
from langchain_core.documents import Document

load_dotenv()


# ============================================================================
# Example: Creating Embeddings and Vector Store
# ============================================================================

print("Example: FAISS Vector Store")
print("=" * 60)

# Sample documents
documents = [
    Document(page_content="Python is a popular programming language.", metadata={"topic": "programming"}),
    Document(page_content="Machine learning is a subset of AI.", metadata={"topic": "AI"}),
    Document(page_content="Cats are popular pets that like to sleep.", metadata={"topic": "animals"}),
    Document(page_content="Dogs are loyal companions.", metadata={"topic": "animals"}),
    Document(page_content="JavaScript is used for web development.", metadata={"topic": "programming"}),
    Document(page_content="Deep learning uses neural networks.", metadata={"topic": "AI"}),
]

# Create embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create vector store from documents
print("Creating vector store...")
vector_store = FAISS.from_documents(documents, embeddings)
print(f"✓ Indexed {len(documents)} documents\n")


# ============================================================================
# Similarity Search
# ============================================================================

print("Similarity Search:")
print("-" * 60)

query = "Tell me about pets"
print(f"Query: '{query}'\n")

# Get top 2 most similar documents
results = vector_store.similarity_search(query, k=2)

for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content} (topic: {doc.metadata['topic']})")

print("\n✓ Found documents about cats and dogs!")
print("✓ Semantic search works without exact keyword matches!\n")


# ============================================================================
# Similarity Search with Scores
# ============================================================================

print("Similarity Search with Scores:")
print("-" * 60)

query2 = "artificial intelligence and neural networks"
results = vector_store.similarity_search_with_score(query2, k=3)

for i, (doc, score) in enumerate(results, 1):
    print(f"{i}. Score: {score:.4f} | {doc.page_content}")

print("\n(Lower scores = more similar in FAISS)")


# ============================================================================
# Save and Load
# ============================================================================

print("\n\nSaving and Loading:")
print("-" * 60)

# Save to disk
vector_store.save_local("my_vector_store")
print("✓ Saved to disk")

# Load from disk
loaded_store = FAISS.load_local(
    "my_vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)
print("✓ Loaded from disk")

# Test
test_results = loaded_store.similarity_search("programming languages", k=1)
print(f"✓ Test query: {test_results[0].page_content}")

# Cleanup
# import shutil
# shutil.rmtree("my_vector_store")
