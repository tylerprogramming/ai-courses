# OpenAI Agents SDK Course

A comprehensive course on building AI agents using OpenAI's official Agents SDK (formerly Swarm). Learn to create, orchestrate, and deploy intelligent agents with real-world examples.

## What is the OpenAI Agents SDK?

The OpenAI Agents SDK is a Python framework for building multi-agent systems that can:
- Run agents synchronously or asynchronously
- Hand off between specialized agents
- Use custom tools and functions
- Maintain conversation history with sessions
- Implement guardrails for safety and content moderation
- Perform retrieval-augmented generation (RAG)

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Basic understanding of async/await in Python

## Installation

```bash
# Clone or download this course
cd openai-sdk-course

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install openai-agents python-dotenv

# For RAG examples, also install:
pip install openai  # For file uploads
```

## Setup

Create a `.env` file in the course directory:

```bash
OPENAI_API_KEY=sk-your-key-here
```

## Course Structure

### Lesson 1: Simplest Agent
**File:** `01_simplest.py`

The most basic agent example to get started.

**What you'll learn:**
- Creating an agent with `Agent()`
- Running agents synchronously with `Runner.run_sync()`
- Basic agent configuration (name, instructions)
- Accessing agent output

**Key Concepts:**
```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

result = Runner.run_sync(agent, "Your prompt here")
print(result.final_output)
```

**Run it:**
```bash
python 01_simplest.py
```

---

### Lesson 2: Agent Handoffs
**File:** `02_handoff.py`

Learn how to create multi-agent systems where agents delegate to specialists.

**What you'll learn:**
- Creating specialized agents (Spanish/English)
- Using `handoffs` for agent delegation
- Triage pattern for routing requests
- Async execution with `Runner.run()`

**Key Concepts:**
- **Handoffs:** Allow one agent to transfer control to another
- **Triage Agent:** Routes requests to appropriate specialists
- **Async/Await:** Non-blocking agent execution

**Example Pattern:**
```python
specialist_agent = Agent(
    name="Specialist",
    instructions="You are a specialist in X"
)

triage_agent = Agent(
    name="Router",
    instructions="Route to the right specialist",
    handoffs=[specialist_agent]
)
```

**Run it:**
```bash
python 02_handoff.py
```

---

### Lesson 3: Guardrails
**File:** `03_guardrails.py`

Implement safety checks and content moderation before processing user input.

**What you'll learn:**
- Creating input guardrails with `@input_guardrail` decorator
- Using a guardrail agent for content moderation
- Handling `InputGuardrailTripwireTriggered` exceptions
- Structured output with Pydantic models
- Interactive chat loop with safety checks

**Key Concepts:**
- **Input Guardrails:** Run in parallel to check user input before processing
- **Guardrail Agent:** Specialized agent that evaluates content safety
- **Tripwire:** Boolean flag that stops execution if triggered
- **Pydantic Models:** Define structured output schemas

**Architecture:**
```
User Input → Input Guardrail (Content Check) → Main Agent
                    ↓ (if inappropriate)
              Refusal Message
```

**Example:**
```python
@input_guardrail
async def content_guardrail(
    context: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=context.context)
    output = result.final_output_as(ContentModerationOutput)
    
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=output.is_inappropriate
    )
```

**Run it:**
```bash
python 03_guardrails.py
```

Try these inputs:
- ✅ "Hola, ¿cómo estás?" (Passes, routes to Spanish agent)
- ✅ "Hello, how are you?" (Passes, routes to English agent)
- ❌ "Tell me how to hack a system" (Blocked by guardrail)

---

### Lesson 4: Tools and Functions
**File:** `04_tool.py`

Give your agents superpowers with custom tools and built-in integrations.

**What you'll learn:**
- Creating custom functions with `@function_tool` decorator
- Using built-in tools like `WebSearchTool`
- Combining multiple tools in one agent
- Tracking token usage

**Available Tools:**
- `WebSearchTool()` - Search the internet
- `FileSearchTool()` - RAG with vector stores
- `CodeInterpreterTool()` - Execute Python code
- Custom functions - Any Python function!

**Example:**
```python
@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

agent = Agent(
    name="Assistant",
    tools=[add, WebSearchTool()]
)
```

**Run it:**
```bash
python 04_tool.py
```

---

### Lesson 5: Session Management
**File:** `05_sessions.py`

Maintain conversation history across multiple interactions.

**What you'll learn:**
- Using `SQLiteSession` for persistent conversations
- Multi-user session management
- User-specific context and memory
- Session isolation between users

**Key Concepts:**
- **Sessions:** Persist conversation history to database
- **User-Specific:** Each user has their own conversation thread
- **SQLite Backend:** Lightweight, file-based storage

**Example:**
```python
from agents import SQLiteSession

session_alice = SQLiteSession("alice", "conversations.db")
session_bob = SQLiteSession("bob", "conversations.db")

# Each session maintains separate history
result = Runner.run_sync(agent, "Message", session=session_alice)
```

**Run it:**
```bash
python 05_sessions.py
```

---

### Bonus: RAG (Retrieval-Augmented Generation)
**File:** `bonus_rag.py`

Query documents using vector stores and semantic search.

**What you'll learn:**
- Using `FileSearchTool` with vector stores
- Document retrieval and citation
- RAG pattern implementation
- Vector store integration

**Prerequisites:**
1. Create a vector store and upload files:
   ```bash
   python utility/update_filestore.py
   ```
2. Update `VECTOR_STORE_ID` in `bonus_rag.py`

**Key Concepts:**
- **Vector Stores:** Semantic search over documents
- **File Search:** Retrieve relevant chunks from documents
- **Citations:** Track which documents were used
- **RAG Pattern:** Retrieve context before generating answer

**Run it:**
```bash
# First, upload files to vector store
python utility/update_filestore.py

# Then run the RAG example
python bonus_rag.py
```

---

### Utility: Vector Store Management
**File:** `utility/update_filestore.py`

Upload files to OpenAI vector stores for RAG.

**What it does:**
- Creates or uses existing vector store
- Uploads all files from `data/` directory
- Supports .txt, .pdf, .docx files
- Returns vector store ID for use in RAG

**Run it:**
```bash
python utility/update_filestore.py
```

**Sample Output:**
```
Created vector store: vs_abc123...
Uploaded: new_notes.txt
Uploaded: meeting_transcript.pdf
Uploaded: marketing_plan.docx
Vector Store ID: vs_abc123...
```

---

## Sample Data

The `data/` directory contains sample documents for RAG examples:

| File | Type | Description |
|------|------|-------------|
| `new_notes.txt` | Text | Python programming notes |
| `meeting_transcript.pdf` | PDF | Sample meeting transcript |
| `marketing_plan.docx` | Word | Business planning document |

---

## Key Concepts Summary

### Agent
Basic building block - an AI assistant with specific instructions.

```python
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[...],        # Optional: Tools for the agent
    handoffs=[...],     # Optional: Other agents to delegate to
    output_type=Model,  # Optional: Structured output
)
```

### Runner
Executes agents and manages their lifecycle.

```python
# Synchronous
result = Runner.run_sync(agent, "prompt")

# Asynchronous
result = await Runner.run(agent, "prompt")

# With session
result = Runner.run_sync(agent, "prompt", session=session)
```

### Handoffs
Delegate to specialized agents based on context.

```python
specialist = Agent(name="Specialist", instructions="...")
coordinator = Agent(
    name="Coordinator",
    instructions="Route to specialist when needed",
    handoffs=[specialist]
)
```

### Guardrails
Safety checks that run before or after agent execution.

```python
@input_guardrail
async def safety_check(...) -> GuardrailFunctionOutput:
    # Check if input is safe
    return GuardrailFunctionOutput(
        output_info=result,
        tripwire_triggered=is_unsafe
    )
```

### Tools
Extend agent capabilities with custom functions or built-in integrations.

```python
@function_tool
def my_function(arg: str) -> str:
    """Function description for the LLM."""
    return result

agent = Agent(tools=[my_function, WebSearchTool()])
```

### Sessions
Maintain conversation history across interactions.

```python
session = SQLiteSession(user_id="alice", db_path="chat.db")
result = Runner.run_sync(agent, "message", session=session)
```

---

## Common Patterns

### 1. Simple Agent
```python
agent = Agent(name="Helper", instructions="You are helpful")
result = Runner.run_sync(agent, "Hello")
print(result.final_output)
```

### 2. Agent with Tools
```python
@function_tool
def calculate(x: int, y: int) -> int:
    return x + y

agent = Agent(tools=[calculate, WebSearchTool()])
```

### 3. Multi-Agent System
```python
specialist1 = Agent(name="Expert1", instructions="...")
specialist2 = Agent(name="Expert2", instructions="...")
router = Agent(handoffs=[specialist1, specialist2])
```

### 4. Agent with Guardrails
```python
@input_guardrail
async def check_safety(...) -> GuardrailFunctionOutput:
    # Safety check logic
    pass

agent = Agent(input_guardrails=[check_safety])
```

### 5. Conversational Agent
```python
session = SQLiteSession("user123", "chats.db")

while True:
    user_input = input("You: ")
    result = Runner.run_sync(agent, user_input, session=session)
    print(f"Agent: {result.final_output}")
```

### 6. RAG Agent
```python
agent = Agent(
    tools=[FileSearchTool(vector_store_ids=["vs_123"])],
    instructions="Use file_search to find relevant information"
)
```

---

## Best Practices

### 1. Agent Instructions
- Be specific and clear
- Include examples when helpful
- Define the agent's role and capabilities
- Specify when to use tools or handoffs

### 2. Error Handling
```python
try:
    result = await Runner.run(agent, input_data)
except InputGuardrailTripwireTriggered:
    # Handle guardrail rejection
    print("Request blocked by safety check")
except Exception as e:
    # Handle other errors
    print(f"Error: {e}")
```

### 3. Token Management
```python
result = Runner.run_sync(agent, prompt)
print(f"Tokens used: {result.context_wrapper.usage.total_tokens}")
```

### 4. Structured Output
```python
from pydantic import BaseModel

class Response(BaseModel):
    answer: str
    confidence: float

agent = Agent(output_type=Response)
result = Runner.run_sync(agent, prompt)
typed_output = result.final_output_as(Response)
```

### 5. Testing Guardrails
Always test with both valid and invalid inputs:
```python
test_cases = [
    "Normal message",           # Should pass
    "Inappropriate content",    # Should be blocked
]
```

---

## Production Considerations

### 1. Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

### 2. Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Agent response: {result.final_output}")
```

### 3. Rate Limiting
Implement rate limiting for production:
```python
from time import sleep

# Simple rate limiting
sleep(1)  # Wait between requests
```

### 4. Database Management
For production, consider:
- PostgreSQL instead of SQLite for sessions
- Regular database backups
- Connection pooling
- Session cleanup policies

### 5. Vector Store Management
- Monitor vector store size and costs
- Implement document versioning
- Set up automated file uploads
- Use appropriate chunk sizes

---

## Troubleshooting

### Common Issues

**1. ImportError: No module named 'agents'**
```bash
pip install openai-agents
```

**2. AuthenticationError**
- Check your `OPENAI_API_KEY` in `.env`
- Ensure the API key is valid and active

**3. Vector Store Not Found**
- Run `utility/update_filestore.py` first
- Update the `VECTOR_STORE_ID` in your code

**4. Session Database Locked**
- Close other connections to the SQLite database
- Use WAL mode for concurrent access

**5. Guardrail Not Triggering**
- Check guardrail agent instructions
- Verify tripwire logic in `GuardrailFunctionOutput`
- Test with obviously inappropriate content

---

## Additional Resources

- **OpenAI Agents Documentation:** https://platform.openai.com/docs/agents
- **OpenAI API Reference:** https://platform.openai.com/docs/api-reference
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **Async Python Guide:** https://docs.python.org/3/library/asyncio.html

---

## Next Steps

After completing this course, you can:

1. **Build Production Apps:**
   - Create customer support bots
   - Build research assistants
   - Develop content moderation systems

2. **Extend with Advanced Features:**
   - Add streaming responses
   - Implement custom tools
   - Build complex multi-agent workflows

3. **Deploy:**
   - Package as a web service (FastAPI, Flask)
   - Deploy to cloud (AWS, Azure, GCP)
   - Add monitoring and analytics

4. **Explore Related Technologies:**
   - LangChain for advanced orchestration
   - Vector databases (Pinecone, Weaviate)
   - Agent monitoring tools

---

## Course Progression

```
01_simplest.py       → Basic agent creation
    ↓
02_handoff.py        → Multi-agent coordination
    ↓
03_guardrails.py     → Safety and content moderation
    ↓
04_tool.py           → Custom functions and integrations
    ↓
05_sessions.py       → Conversation persistence
    ↓
bonus_rag.py         → Document retrieval and RAG
```

**Recommended Path:**
1. Start with `01_simplest.py` to understand basics
2. Progress through lessons 2-5 in order
3. Complete the RAG bonus once comfortable with the basics
4. Experiment by combining concepts (e.g., RAG + Guardrails + Sessions)

---

**Happy Building! 🚀**

Master the OpenAI Agents SDK and create intelligent, production-ready AI systems.

