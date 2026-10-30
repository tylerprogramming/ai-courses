# LlamaParse Course

Two scripts that parse `data/us-gov.pdf` with [LlamaParse](https://www.llamaindex.ai/llamaparse) and query it with LlamaIndex.

| Script | What it does | Keys needed |
| --- | --- | --- |
| `01_starter.py` | Parses the PDF to markdown and prints each page's text, markdown, images, layout and structured data. | LlamaCloud |
| `02_advanced_rag.py` | Parses the PDF in agent mode (high-res OCR, multi-page tables, screenshots), builds a vector index in `storage/`, then opens an interactive query loop answered by `gpt-4o`. | LlamaCloud + OpenAI |

## Setup and run

Needs Python 3.10 or newer.

```bash
cd llamaparse-course
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```bash
LLAMA_PARSE_API_KEY=llx-...   # from https://cloud.llamaindex.ai, read by both scripts
OPENAI_API_KEY=sk-...         # used by 02_advanced_rag.py for embeddings and gpt-4o
```

Then run either script from this folder (both use the relative path `data/us-gov.pdf`):

```bash
python 01_starter.py
python 02_advanced_rag.py   # type a question, or quit to exit
```

`storage/` already holds an index of `data/us-gov.pdf`. `02_advanced_rag.py` checks the PDF's SHA-256 against `storage/document_hash.json` and, while they match, loads that index instead of parsing again, so the first run only needs the OpenAI key. If you change the PDF, the script deletes `storage/` and rebuilds it, which spends LlamaCloud parsing credits (agent mode is the most expensive tier).

## Note on the LlamaParse SDK

These scripts use `from llama_parse import LlamaParse`. LlamaIndex has deprecated the `llama-parse` and `llama-cloud-services` packages (maintenance was promised until May 1, 2026) in favour of the unified `llama-cloud>=1.0` SDK and the Parse v2 API, where `parse_mode` becomes `tier` (`fast`, `cost_effective`, `agentic`, `agentic_plus`). `llama-parse` 0.6.94 (February 2026) is the last release; it still installs and imports, and prints a `DeprecationWarning` on import. The code here is kept as shown in the course. For new projects, see the [Parse getting started guide](https://developers.llamaindex.ai/llamaparse/parse/getting_started/) and the [v1 to v2 migration guide](https://developers.llamaindex.ai/llamaparse/parse/guides/migration-v1-to-v2/).
