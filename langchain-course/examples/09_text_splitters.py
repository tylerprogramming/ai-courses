"""
Topic 9: Text Splitters (Chunking)

Text splitters break large documents into chunks for:
- Fitting within LLM context windows
- Creating better embeddings
- Improving RAG retrieval accuracy

Use RecursiveCharacterTextSplitter (recommended)
"""

import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Alternative: CharacterTextSplitter (simpler but less smart)
from langchain_core.documents import Document

load_dotenv()


# Sample document
text = """
Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that focuses on building
systems that can learn from data. Instead of being explicitly programmed to perform
a task, these systems improve their performance through experience.

Types of Machine Learning

There are three main types of machine learning:

Supervised Learning: In supervised learning, the algorithm learns from labeled training
data. The system is provided with input-output pairs and learns to map inputs to outputs.
Common applications include image classification, spam detection, and price prediction.

Unsupervised Learning: Unsupervised learning works with unlabeled data. The algorithm
tries to find patterns and structure in the data without predefined labels. Clustering
and dimensionality reduction are common unsupervised learning tasks.

Reinforcement Learning: In reinforcement learning, an agent learns to make decisions
by interacting with an environment. The agent receives rewards or penalties based on
its actions and learns to maximize cumulative rewards over time.
"""

doc = Document(page_content=text.strip(), metadata={"source": "ml_intro.txt"})


# ============================================================================
# Example: RecursiveCharacterTextSplitter (RECOMMENDED)
# ============================================================================

print("Example: RecursiveCharacterTextSplitter")
print("=" * 60)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Max characters per chunk
    chunk_overlap=50,      # Overlap between chunks (preserves context)
    length_function=len,
)

chunks = splitter.split_documents([doc])

print(f"Split into {len(chunks)} chunks\n")

for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i} ({len(chunk.page_content)} chars):")
    print(chunk.page_content[:150] + "...\n")
    print(f"Metadata: {chunk.metadata}\n")
    print("-" * 60)


# ============================================================================
# How RecursiveCharacterTextSplitter Works
# ============================================================================

print("\nHow it works:")
print("-" * 60)
print("""
RecursiveCharacterTextSplitter tries separators in order:
1. "\\n\\n" (paragraphs) - try first
2. "\\n" (lines) - if chunks still too large
3. " " (words) - if still too large
4. "" (characters) - last resort

This preserves semantic meaning better than simple character splitting!
""")


# ============================================================================
# Chunk Size Guidelines (2025)
# ============================================================================

print("\nChunk Size Guidelines:")
print("-" * 60)
print("""
General purpose:     500-1000 characters
Q&A systems:         500-1000 characters
Book summarization:  1000-2000 characters
Technical docs:      500-800 characters
Code documentation:  300-600 characters

Overlap: 10-20% of chunk_size (e.g., 100-200 for size=1000)

Test with your data to find optimal settings!
""")

print("\n✓ Use RecursiveCharacterTextSplitter (default)")
print("✓ Typical: chunk_size=1000, overlap=200")
print("✓ Balance precision vs. context")
print("✓ Next: 10_vector_stores.py")
