"""
Topic 8: Document Loaders

Document loaders convert various sources (PDFs, websites, CSVs, etc.)
into LangChain's Document format.

200+ loaders available!
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, CSVLoader, WebBaseLoader
from langchain_core.documents import Document

load_dotenv()


# ============================================================================
# Example 1: TextLoader
# ============================================================================

# Create sample file
sample_text = """LangChain: The OG Orchestration Framework

LangChain is a framework for building applications with LLMs.
Key features: 300+ LLM integrations, LCEL, agents, RAG, and more.

LangChain 1.0 released October 2025 with stability commitment."""

with open("sample_document.txt", "w") as f:
    f.write(sample_text)

print("Example 1: TextLoader")
print("-" * 60)

loader = TextLoader("sample_document.txt")
documents = loader.load()

doc = documents[0]
print(f"Loaded {len(documents)} document(s)")
print(f"Content: {doc.page_content[:100]}...")
print(f"Metadata: {doc.metadata}")


# ============================================================================
# Example 2: CSVLoader
# ============================================================================

csv_content = """name,role,technology
Alice,Data Scientist,Python
Bob,ML Engineer,TensorFlow
Charlie,Developer,LangChain"""

with open("sample_data.csv", "w") as f:
    f.write(csv_content)

print("\n\nExample 2: CSVLoader (each row = document)")
print("-" * 60)

loader = CSVLoader("sample_data.csv")
documents = loader.load()

print(f"Loaded {len(documents)} documents")
for i, doc in enumerate(documents[:2], 1):
    print(f"{i}. {doc.page_content}")


# ============================================================================
# Example 3: WebBaseLoader
# ============================================================================

print("\n\nExample 3: WebBaseLoader")
print("-" * 60)

try:
    loader = WebBaseLoader("https://docs.langchain.com/oss/python/langchain/overview")
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s) from web")
    print(f"First 100 chars: {documents[0].page_content[:100]}...")
except Exception as e:
    print(f"(Skipped - requires internet: {e})")

# Cleanup
# os.remove("sample_document.txt")
# os.remove("sample_data.csv")
