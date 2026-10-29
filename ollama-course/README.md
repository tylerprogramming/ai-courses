# Ollama Course

Three small scripts that call models through [Ollama](https://ollama.com): the
Python client, a LangChain agent, and an Ollama Cloud model.

| Script | What it shows | Model |
| --- | --- | --- |
| `simple_request.py` | One chat call with the `ollama` Python client | `gemma3:1b` (local) |
| `langchain_ollama_request.py` | A LangChain `create_agent` agent backed by `ChatOllama` | `deepseek-r1:1.5b` (local) |
| `ollama_cloud.py` | Streams a reply from a cloud-hosted model | `gpt-oss:120b-cloud` |

## Setup

1. Install Ollama from https://ollama.com/download and start it (`ollama serve`,
   or open the desktop app).
2. Pull the local models:

   ```bash
   ollama pull gemma3:1b
   ollama pull deepseek-r1:1.5b
   ```

3. For `ollama_cloud.py`, sign in so your local Ollama can reach cloud models:

   ```bash
   ollama signin
   ```

   The script uses `Client()` with no host, so it talks to your local Ollama,
   which forwards `-cloud` models to Ollama Cloud.

4. Install the Python packages (Python 3.10 or newer):

   ```bash
   cd ollama-course
   pip install -r requirements.txt
   ```

## Run

```bash
python simple_request.py
python langchain_ollama_request.py
python ollama_cloud.py
```

No API keys are needed for the local scripts. Set `OLLAMA_HOST` if Ollama is not
on `http://localhost:11434`.
