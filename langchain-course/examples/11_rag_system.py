"""
Topic 11: Complete RAG System

RAG (Retrieval Augmented Generation) = Retrieval + Generation
Allows LLMs to access external knowledge and provide grounded answers.

This combines EVERYTHING:
- Document loaders → Text splitters → Embeddings → Vector store → Retrieval → Generation
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


# ============================================================================
# Step 1: Create Knowledge Base
# ============================================================================

print("Step 1: Creating Knowledge Base")
print("=" * 60)

documents = [
    Document(
        page_content="""TechCorp is a leading software company founded in 2010 by Jane Smith
and John Doe. We specialize in AI-powered business solutions with over 500 employees
worldwide. Our headquarters is in San Francisco, California.""",
        metadata={"source": "company_overview.txt"}
    ),
    Document(
        page_content="""Our flagship product is BusinessAI, an AI platform for automating
business processes. Features include automated document processing, intelligent chatbots,
predictive analytics, and natural language querying. Pricing starts at $99/month with a
free 14-day trial.""",
        metadata={"source": "products.txt"}
    ),
    Document(
        page_content="""Customer support available via email (support@techcorp.com) 24/7,
phone (1-800-TECH-CORP) Mon-Fri 9am-5pm PST, and live chat during business hours.
Average response time: 2 hours for email, immediate for live chat.""",
        metadata={"source": "support.txt"}
    ),
    Document(
        page_content="""Q4 2024 Results: Revenue $50M (up 25% YoY), 1,200 new customers,
launched BusinessAI 3.0, opened offices in London and Tokyo. Awards: Best AI Platform
2024 by TechReview Magazine.""",
        metadata={"source": "news.txt"}
    ),
]

print(f"✓ Created {len(documents)} knowledge base documents\n")


# ============================================================================
# Step 2: Build RAG Pipeline
# ============================================================================

print("Step 2: Building RAG Pipeline")
print("=" * 60)

# 1. Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(documents)
print(f"✓ Split into {len(splits)} chunks")

# 2. Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(splits, embeddings)
print(f"✓ Indexed in FAISS")

# 3. Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 4})  # Top 3 chunks
print(f"✓ Created retriever")

# 4. Create RAG prompt
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant for TechCorp.
Answer questions based on the provided context.
If the answer is not in the context, say "I don't have that information."

Context:
{context}
"""),
    ("human", "{question}")
])

# 5. Create LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 6. Build the RAG chain with LCEL
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

print(f"✓ Built RAG chain: retriever | format | prompt | llm | parser\n")


# ============================================================================
# Step 3: Test RAG System
# ============================================================================

print("Step 3: Testing RAG System")
print("=" * 60)

questions = [
    "Who founded TechCorp?",
    "What products does TechCorp offer?",
    "How can I contact customer support?",
    "What were Q4 2024 results?",
    "What is the refund policy?",  # Not in knowledge base
]

for question in questions:
    print(f"\nQ: {question}")

    # Show retrieved docs
    retrieved = retriever.invoke(question)
    print(f"Retrieved from: {[d.metadata['source'] for d in retrieved]}")

    # Get answer
    answer = rag_chain.invoke(question)
    print(f"A: {answer}")
    print("-" * 60)


# =======
# INDEXING (one-time):
#   Documents → Splitter → Chunks → Embeddings → Vector Store

# RETRIEVAL-GENERATION (per query):
#   Question → Embedding → Similarity Search → Top K Chunks
#   Chunks + Question → LLM → Answer

# BENEFITS:
# ✓ Access to private/recent data
# ✓ Grounded answers (not hallucinated)
# ✓ Source attribution
# ✓ Up-to-date without retraining
# ✓ 70% accuracy improvement for domain-specific queries
