# Quick Start Guide

Get started with the LangChain crash course in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

```bash
# 1. Navigate to the course directory
cd langchain-course

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

## Configuration

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env and add your OpenAI API key
# Replace "your-openai-api-key-here" with your actual key
```

Or set it directly:
```bash
# macOS/Linux:
export OPENAI_API_KEY="your-key-here"

# Windows:
set OPENAI_API_KEY=your-key-here
```

## Run Your First Example

```bash
# Start with the basics
python examples/01_agent_basics.py
```

If you see output without errors, you're all set! 🎉

## Follow the Course

Work through the examples in order:

```bash
python examples/01_agent_basics.py            # create_agent with a tool
python examples/02_agent_structured_output.py # Structured output
python examples/03_agent_middleware.py        # Middleware (summarization)
python examples/04_agents_with_memory.py      # Memory with a checkpointer
```

`examples/05_agents_advanced.py` is a sub-agent pattern sketch with placeholder model and tools; fill them in before running it.

Each example is self-contained and includes explanations!

## Troubleshooting

### "Module not found" error
Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### "OpenAI API key not found" error
Make sure you set your API key:
```bash
export OPENAI_API_KEY="your-key-here"
```
Or create a `.env` file with the key.

### Rate limit errors
If you're on the free tier, you may hit rate limits. Wait a few moments and try again.

## What's Next?

After completing the examples:
1. Read the main [README.md](README.md) for detailed information
2. Experiment with your own documents and use cases
3. Explore [LangGraph](https://langchain-ai.github.io/langgraph/) for multi-agent systems
4. Check out [LangSmith](https://smith.langchain.com) for monitoring

## Need Help?

- 📖 Official Docs: https://docs.langchain.com
- 💬 GitHub Issues: https://github.com/langchain-ai/langchain/issues
- 🌟 Star the repo: https://github.com/langchain-ai/langchain

Happy learning! 🚀
