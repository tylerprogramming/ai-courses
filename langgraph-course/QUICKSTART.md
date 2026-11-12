# LangGraph Quick Start (10 Minutes)

Get up and running with LangGraph in 10 minutes!

## Step 1: Setup (3 minutes)

```bash
# Navigate to course directory
cd langgraph-course

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (2 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Run Examples (5 minutes)

```bash
# Example 1: Graph API (state, nodes, conditional edges, tool loop)
python examples/01_graph_api_basics.py

# Example 2: Functional API (@task / @entrypoint, streaming)
python examples/02_functional_api.py
```

Example 3 is a client for a local LangGraph server, so start the server first in a second terminal:

```bash
pip install -U "langgraph-cli[inmem]"
cd my-agent-app
pip install -e .
# add OPENAI_API_KEY=... to my-agent-app/.env
langgraph dev            # serves the "agent" graph on http://localhost:2024
```

Then, back in `langgraph-course/`:

```bash
python examples/03_local_test.py
```

## What Just Happened?

### 01_graph_api_basics.py
You learned:
- ✓ State with TypedDict and Annotated reducers
- ✓ Nodes, edges and conditional routing
- ✓ An agent loop that calls tools

### 02_functional_api.py
You learned:
- ✓ @task and @entrypoint
- ✓ Agent loops in plain Python
- ✓ Streaming execution

### 03_local_test.py
You learned:
- ✓ Running a graph behind `langgraph dev`
- ✓ Streaming a run from the Python SDK (`langgraph_sdk.get_client`)

## Course Structure

Only **3 files** to master LangGraph:

1. **01_graph_api_basics.py** - Graph API (15-20 min) ⭐
2. **02_functional_api.py** - Functional API (15-20 min) ⭐⭐
3. **03_local_test.py** - Local server client (20-30 min) ⭐⭐⭐

**Total time**: 1-2 hours

## Common Issues

### Import Errors
```bash
pip install --upgrade langgraph langchain-openai
```

### API Key Not Found
Make sure `.env` file exists and contains `OPENAI_API_KEY=your-key`

### Module Not Found
Make sure virtual environment is activated:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

## Tips

1. **Run each file completely** - Don't skip ahead
2. **Read the output** - Understand what's happening
3. **Modify and experiment** - Best way to learn!
4. **Check the comments** - They explain the concepts

## Next Steps

After completing all 3 examples:
- Build your own graph-based workflow
- Implement a multi-agent system
- Deploy a production LangGraph app

## Need Help?

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [GitHub Issues](https://github.com/langchain-ai/langgraph/issues)

**Ready? Start with `examples/01_graph_api_basics.py`!** 🚀
