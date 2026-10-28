# smolagents course

Five short scripts for Hugging Face [smolagents](https://github.com/huggingface/smolagents).

| Script | What it shows | Needs |
|---|---|---|
| `01_first.py` | A `CodeAgent` with no tools | `HF_TOKEN` |
| `02_tools.py` | `CodeAgent` with `DuckDuckGoSearchTool` | `HF_TOKEN` |
| `03_custom_tools.py` | A `@tool` that finds the most downloaded Hub model for a task | `HF_TOKEN` |
| `04_e2b.py` | Runs the agent's code in an E2B sandbox (`executor_type="e2b"`) | `HF_TOKEN`, `E2B_API_KEY` |
| `05_mult-agent.py` | A manager `CodeAgent` that calls a web-search `ToolCallingAgent` | `HF_TOKEN` |

## Run

```bash
cd smolagents-course
pip install -r requirements.txt
hf auth login            # or put HF_TOKEN=... in a .env file
python 01_first.py
```

## Model

The scripts use `InferenceClientModel(model_id=HF_MODEL_ID)` with
`HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"`. The smolagents 1.26 default,
`Qwen/Qwen3-Next-80B-A3B-Thinking`, is not in the Inference Providers router's model list and its only
provider mapping reports an error, so a bare `InferenceClientModel()` is not expected to work.
To try another model, change `HF_MODEL_ID` to any chat model listed at
https://router.huggingface.co/v1/models.
