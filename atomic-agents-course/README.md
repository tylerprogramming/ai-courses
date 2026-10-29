# Atomic Agents Crash Course (10 Minutes)

## What is Atomic Agents?

Atomic Agents is a **lightweight, modular Python framework** for building AI-powered applications with **structured inputs and outputs**. Unlike autonomous multi-agent frameworks that prioritize autonomy, Atomic Agents emphasizes **control, predictability, and maintainability** for production applications.

Built on top of [Instructor](https://github.com/jxnl/instructor) and [Pydantic](https://docs.pydantic.dev/), it provides a clean, composable approach to building AI agents.

## Design Philosophy: "Do One Thing Well"

The framework follows an **atomicity model** where each component:
- **Does one thing well** - focused, single-responsibility components
- **Is reusable** - works across different pipelines
- **Composes easily** - components snap together like building blocks
- **Produces consistent results** - structured I/O ensures reliability

## Core Concepts

### 1. AtomicAgent
The central unit that processes inputs through a defined schema. Think of it as a function with:
- **Structured Input** (Pydantic model)
- **LLM Processing** (with system prompt)
- **Structured Output** (Pydantic model)

### 2. Input/Output Schemas
Pydantic-based structures that define **data contracts** between components. This ensures type safety and validation.

### 3. SystemPromptGenerator
Builds prompts from:
- Background information
- Step-by-step instructions
- Output format requirements

### 4. AgentConfig
Configuration container specifying:
- LLM client (OpenAI, Groq, etc.)
- Model name
- System prompt
- Conversation history

### 5. Context Providers (Advanced)
Dynamic information injectors that enhance prompts at runtime without modifying core agent logic. Examples: search results, user data, database queries.

## How It Works

```
Input (Pydantic) → Agent + System Prompt → LLM → Output (Pydantic)
```

1. Define your input/output schemas using Pydantic
2. Configure your agent with an LLM client
3. Create a system prompt describing the agent's task
4. Call the agent with structured input
5. Receive validated structured output

## Installation

Atomic Agents 2.x needs Python 3.12 or newer.

```bash
cd atomic-agents-course
pip install -r requirements.txt
```

Then put your key in a `.env` file in this folder:

```bash
OPENAI_API_KEY=your_api_key_here
```

For other providers (Groq, Anthropic, Gemini), install the matching instructor extra, e.g. `pip install "instructor[anthropic]"`.

## The 3 Examples

### Example 1: Basic Agent (`01_basic_agent.py`)
- Create a simple agent that analyzes sentiment
- Learn the fundamental structure: Input → Agent → Output
- Understand schemas and agent configuration

### Example 2: Agent with Tools (`02_agent_with_tools.py`)
- Add tool-calling capabilities to your agent
- Agent can decide when to use tools
- Learn how tools integrate with the agent workflow

### Example 3: Chaining Schemas (`03_modular_example.py`)
- Point an agent's output schema at a tool's input schema
- Swap one search tool for another by changing the schema
- See how agents and tools compose together

This one is a reading example, not a runnable script. It is the "Chaining Schemas and Agents" snippet from the [Atomic Agents README](https://github.com/BrainBlend-AI/atomic-agents#chaining-schemas-and-agents), and it imports `web_search_agent.tools...`, which lives in the upstream repo's [web-search-agent example](https://github.com/BrainBlend-AI/atomic-agents/tree/main/atomic-examples/web-search-agent), not in this folder or on PyPI. `SomeSearchTool` stands in for whichever tool you swap in.

## Key Takeaways

1. **Structured I/O** - Pydantic schemas ensure reliability
2. **Composability** - Agents are building blocks
3. **Production-Ready** - Emphasizes control over autonomy
4. **Framework-Agnostic** - Works with any Instructor-supported LLM provider

## Next Steps

Run the examples in order (example 3 is for reading, see above):
```bash
python 01_basic_agent.py
python 02_agent_with_tools.py
```

## Resources

- GitHub: https://github.com/BrainBlend-AI/atomic-agents
- Documentation: https://atomic-agents.io
- Instructor: https://github.com/jxnl/instructor
- Pydantic: https://docs.pydantic.dev/
