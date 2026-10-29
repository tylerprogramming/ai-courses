## 🔍 Background & Why It Matters

LlamaIndex is an open-source framework for building LLM-powered applications over your own data—such as documents, PDFs, databases, and more.

Its main value is context augmentation via retrieval-augmented generation (RAG): you index your data, then at query time you retrieve relevant chunks and feed them into the LLM.

LlamaIndex provides building blocks for data ingestion, indexing, querying, workflows, and agentic applications.

### Why It’s Great

- **Developer-first:** Python & TypeScript SDKs.
- **Large community:** The GitHub repo has ~45k stars.
- **Integrates well:** Works with vector stores, tool-calls, workflows, and agents.
- **Build “agent over your data” apps** (not just generic chatbots).

---

## 📌 What It’s Mainly Used For

- Document Q&A (upload PDFs/DOCX, ask questions)
- Chatbots over internal company data (SOPs, spreadsheets, CRM, etc.)
- Retrieval-augmented generation (RAG) workflows
- Agentic systems where the LLM chooses tools, retrieves data, acts, and returns results
- Multi-agent workflows (example repos exist with complex agent pipelines)

---

## 🔧 Key Concepts & Components

Understand these core concepts:

- **Data connectors / loaders:** Bring in files, databases, APIs.
- **Indices:** Create an index of your data—vector, list, or tree index.
- **Query engines:** Use the index to answer queries.
- **Retrieval + LLM:** Retrieve relevant nodes and call the LLM with the associated context.
- **Agents / Workflows:** Use the `Workflow` class and agent abstractions (composed of tools, loops, memory).
- **Tool integration:** Agents can call functions/tools, and the framework supports dynamic tool routing.
- **Reasoning loops / multi-step logic:** Agents can determine the next step, use a tool, reflect, and loop as needed.

---

## ▶️ Setup and Run

Needs Python 3.10 or newer and an OpenAI key. The scripts use `gpt-4o-mini` for chat and LlamaIndex's default OpenAI embedding model for indexing.

```bash
cd llamaindex-course
pip install -r requirements.txt
```

Then create a `.env` file in this folder with `OPENAI_API_KEY=your_api_key_here`.

Run the scripts from this folder, since they read `data/docs` and `storage` by relative path:

| Script | What it shows |
| --- | --- |
| `01_first.py` | Index `data/docs` and chat with it (type `exit` to quit) |
| `02_llama_hub.py` | Load the Ars Technica RSS feed with `RssReader` from LlamaHub and chat with it |
| `03_agents.py` | A `FunctionAgent` with a `multiply` tool |
| `04_agent_memory.py` | An agent with a calculator and a document-search tool. It reuses the saved index in `storage/` if present, otherwise it builds and saves one |

`03_agents.py` does not call `load_dotenv()`, so export `OPENAI_API_KEY` in your shell (or add `load_dotenv()`) before running it.

If you change the files in `data/docs`, delete `storage/` so `04_agent_memory.py` rebuilds the index.