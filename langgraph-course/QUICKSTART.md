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
# Example 1: Basics (graphs, state, routing)
python examples/01_basics.py

# Example 2: Agents (tools, multi-agent)
python examples/02_agents.py

# Example 3: Production (persistence, human-in-loop, RAG)
python examples/03_production.py
```

## What Just Happened?

### 01_basics.py
You learned:
- ✓ How to build graphs with nodes and edges
- ✓ State management with reducers
- ✓ Conditional routing
- ✓ Loops

### 02_agents.py
You learned:
- ✓ Agents with tools (calculator, weather)
- ✓ Multi-agent systems (researcher + writer)
- ✓ Agent coordination

### 03_production.py
You learned:
- ✓ Persistence (save/resume conversations)
- ✓ Human-in-the-loop approval
- ✓ RAG with vector search

## Course Structure

Only **3 files** to master LangGraph:

1. **01_basics.py** - Foundation (15-20 min) ⭐
2. **02_agents.py** - Agents (20-30 min) ⭐⭐
3. **03_production.py** - Production (30-40 min) ⭐⭐⭐

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

**Ready? Start with `examples/01_basics.py`!** 🚀
