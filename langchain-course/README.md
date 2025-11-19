# LangChain Crash Course 2025 - Essentials + RAG

## What is LangChain?

LangChain is the **OG orchestration framework** for building applications with Large Language Models (LLMs). Originally released in 2022, it has become the most popular framework for LLM application development with over **70 million downloads per month** (more than the OpenAI SDK!).

### Core Philosophy

LangChain provides:
- **Provider-agnostic abstractions** - Work with 300+ LLM providers through a single interface
- **Modular building blocks** - Chains, agents, tools, memory, retrievers, and more
- **Production-ready tools** - From development to deployment with LangSmith and LangGraph
- **Massive ecosystem** - 600+ integrations with vector databases, APIs, document loaders, and tools

### Main Components

1. **LangChain Core** - The foundation with abstractions and LCEL
2. **LangGraph** - Stateful multi-agent framework (GA v1.0 in 2025)
3. **LangSmith** - Debugging, monitoring, and evaluation platform
4. **Integration Packages** - Provider-specific packages (langchain-openai, langchain-anthropic, etc.)

---

## What's New in 2025?

### LangChain 1.0 (Released October 22, 2025)

LangChain reached its **first stable release** with major improvements:

#### 1. **New Agent Abstraction**
- `create_agent` and `create_react_agent` for fastest agent building
- Enhanced structured outputs integrated into agent loop
- Reduced latency and costs by eliminating extra LLM calls

#### 2. **Middleware Support**
- Custom middleware can hook into any point in agent execution
- Enables human-in-the-loop review, auto-summarization, PII redaction
- Better control over agent behavior

#### 3. **Standardized Content Blocks**
- New `.content_blocks` property on messages
- Fully typed view of message content
- Standardizes reasoning traces, citations, server-side tool calls, multi-modal content

#### 4. **Reduced Package Scope**
- Core package focused on essential abstractions
- Legacy functionality moved to `langchain-classic`
- Lightweight integration packages separately maintained

#### 5. **Stability Commitment**
- **No breaking changes until 2.0** - Safe for production use
- Python 3.10+ required (3.9 dropped due to EOL)

### Recent Updates (2025)

**March 2025:**
- **Standardized forced tool calling** across all providers
- **Universal token counting** - Track usage across all models
- **OpenTelemetry support** in LangSmith for integration with Datadog, Grafana, Jaeger

**November 2025:**
- Latest version: **1.0.7** (released Nov 14, 2025)
- Continuous improvements and bug fixes

---

## How LangChain Has Changed

### The Evolution

**Early Days (2022-2023):**
- Focused on chains and simple LLM workflows
- Rapid growth but breaking changes
- Community-driven development

**Maturity Phase (2024):**
- Introduction of LCEL (modern syntax)
- LangGraph for complex agents
- LangSmith for observability
- Preparation for 1.0

**Stable Era (2025):**
- Production-ready with 1.0 release
- No breaking changes commitment
- Enterprise adoption at scale (85M+ users in single deployment)
- Nearly 400 companies using LangGraph in production

### Key Paradigm Shifts

#### 1. **Legacy Chains → LCEL (LangChain Expression Language)**

**Old Way:**
```python
# LLMChain - deprecated
from langchain.chains import LLMChain
chain = LLMChain(llm=model, prompt=prompt)
```

**New Way (2025):**
```python
# LCEL - modern, recommended approach
chain = prompt | model | parser  # Clean pipe operator syntax
```

**Why LCEL?**
- Clean, composable syntax
- Built-in streaming support
- Async capabilities
- Better performance
- Easier debugging

#### 2. **Simple Agents → LangGraph for Complex Workflows**

**When to Use What:**
- **LCEL**: Simple chains, basic retrieval, linear workflows
- **LangGraph**: Complex workflows, multi-agent systems, stateful applications, cycles/branching

#### 3. **Manual Debugging → LangSmith Observability**

**Before:**
- Print statements
- Manual logging
- Hard to trace issues

**Now (2025):**
- Complete execution traces
- Real-time monitoring
- Token counting and cost tracking
- A/B testing and evaluation
- OpenTelemetry integration

#### 4. **Monolithic Package → Modular Architecture**

**Old Structure:**
- Everything in one package
- Heavy dependencies
- Tightly coupled

**New Structure (2025):**
```
langchain (core abstractions + LCEL)
├── langchain-openai (OpenAI integration)
├── langchain-anthropic (Anthropic integration)
├── langchain-google-genai (Google integration)
└── langchain-community (community integrations)
```

**Benefits:**
- Install only what you need
- Independent versioning
- Better compatibility
- Reduced dependency bloat

---

## Course Overview

This crash course covers **Essentials + RAG** - everything you need to build real LangChain applications in 2025.

### Topics Covered

#### **Essentials (Topics 1-5)**
1. **Basic Setup & Installation** - Get started with LangChain 1.0
2. **LCEL Basics** - Modern chain building with pipe operators
3. **Tool Calling** - Connect LLMs to external functions and APIs
4. **Prompts & Templates** - Dynamic prompt construction
5. **Agents** - ReAct agents that reason and act

#### **Memory & Conversation (Topics 6-7)**
6. **Memory Systems** - Maintain conversation history
7. **Building a Chatbot** - Conversational AI with context

#### **RAG - Retrieval Augmented Generation (Topics 8-11)**
8. **Document Loaders** - Load data from 200+ sources
9. **Text Splitters** - Chunk documents intelligently
10. **Vector Stores** - Semantic search with embeddings
11. **Building a RAG System** - Complete Q&A over documents

---

## Course Structure

```
langchain-course/
├── README.md (this file)
├── requirements.txt
└── examples/
    ├── 01_setup.py
    ├── 02_lcel_basics.py
    ├── 03_tool_calling.py
    ├── 04_prompts_templates.py
    ├── 05_agents.py
    ├── 06_memory.py
    ├── 07_chatbot.py
    ├── 08_document_loaders.py
    ├── 09_text_splitters.py
    ├── 10_vector_stores.py
    └── 11_rag_system.py
```

---

## Prerequisites

- Python 3.10 or higher
- Basic Python knowledge
- API key for an LLM provider (OpenAI recommended for this course)
- Understanding of LLMs and embeddings (helpful but not required)

---

## Installation

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export OPENAI_API_KEY="your-api-key-here"  # On Windows: set OPENAI_API_KEY=your-api-key-here
```

---

## Quick Start

Each example file is self-contained and can be run independently:

```bash
# Run any example
python examples/01_setup.py
python examples/02_lcel_basics.py
# ... etc
```

Follow the examples in order for the best learning experience!

---

## Key Takeaways for 2025

1. **LangChain 1.0 is production-ready** - Stable API, no breaking changes commitment
2. **Use LCEL, not legacy chains** - Modern syntax with pipe operators
3. **LangGraph for complex agents** - When you need stateful, multi-step workflows
4. **LangSmith is essential** - Debugging and monitoring from day one
5. **Provider-agnostic design** - Easy to swap between OpenAI, Anthropic, Google, etc.
6. **RAG is powerful** - Up to 70% accuracy improvement for domain-specific queries
7. **Massive ecosystem** - 600+ integrations, don't reinvent the wheel

---

## Resources

- **Official Docs**: https://docs.langchain.com
- **API Reference**: https://python.langchain.com/api_reference
- **Changelog**: https://changelog.langchain.com
- **GitHub**: https://github.com/langchain-ai/langchain
- **LangSmith**: https://smith.langchain.com

---

## What's Next?

After completing this course, explore:
- **LangGraph** - Build complex multi-agent systems
- **LangSmith** - Advanced monitoring and evaluation
- **Advanced RAG** - Adaptive RAG, Long RAG (25,000+ tokens)
- **Production Deployment** - Scale your applications
- **Custom Tools** - Build domain-specific integrations

---

**Let's get started! Head to `examples/01_setup.py` to begin.**
