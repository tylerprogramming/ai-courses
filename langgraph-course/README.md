# LangGraph Crash Course (2025)

**Build stateful, graph-based agent workflows with LangGraph**

LangGraph is a framework for creating stateful, graph-based agent systems. It provides two APIs for building workflows: Graph API (declarative) and Functional API (imperative).

## What is LangGraph?

LangGraph extends LangChain with:
- **Stateful workflows**: Maintain state across multiple steps
- **Graph-based orchestration**: Define workflows as nodes and edges
- **Two APIs**: Graph API (explicit structure) or Functional API (Python control flow)
- **Agent loops**: Built-in support for ReAct patterns
- **Tool execution**: Seamless tool calling and result handling
- **Local server**: Run agents as web API for visual debugging

## Course Structure (3 Files)

Based on the official LangGraph quickstart documentation.

### **01_graph_api_basics.py** ⭐
**Graph API Pattern**
- State with TypedDict and Annotated
- Nodes, edges, and conditional routing
- StateGraph builder pattern
- Tool execution in graphs

*Time: 15-20 minutes*

### **02_functional_api.py** ⭐⭐
**Functional API Pattern**
- @task and @entrypoint decorators
- Python control flow (while loops)
- Streaming agent execution
- Concise agent implementation

*Time: 15-20 minutes*

### **03_local_server_setup.py** ⭐⭐⭐
**Local Server (Production Preview)**
- Run graphs as web API
- Visual debugging with Studio UI
- Persistent conversations
- Multiple client access

*Time: 20-30 minutes*

## Quick Start

```bash
# 1. Navigate to course directory
cd langgraph-course

# 2. Create virtual environment (if needed)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run examples in order
python examples/01_graph_api_basics.py
python examples/02_functional_api.py
python examples/03_local_server_setup.py
```

## Two APIs, Same Power

### Graph API (Declarative)
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("llm", llm_node)
graph.add_node("tools", tools_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", router, ["tools", END])
agent = graph.compile()
```

**Best for:**
- Complex branching workflows
- Visual workflow representation
- Multiple agents with routing
- Human-in-the-loop patterns

### Functional API (Imperative)
```python
from langgraph.func import entrypoint, task

@task
def call_llm(messages):
    return model.invoke(messages)

@entrypoint()
def agent(messages):
    response = call_llm(messages).result()
    while response.tool_calls:
        # Execute tools, loop back
    return messages
```

**Best for:**
- Simple agent loops
- Standard Python control flow
- Quick prototyping
- ReAct-style agents

---

## LangGraph Local Server (Production Preview)

Run your graphs as a web API for visual debugging and testing before deployment.

### What You Get

- 🌐 **Web API** at `http://localhost:2024`
- 🎨 **Visual Studio UI** for debugging
- 💾 **Persistent conversations** with thread IDs
- 🔌 **Multiple clients**: Python SDK, REST API, Web UI

### Quick Setup (5 minutes)

#### 1. Install CLI

```bash
pip install -U "langgraph-cli[inmem]"
```

**Requirements**: Python 3.11+

#### 2. Create Project

```bash
langgraph new my-agent --template new-langgraph-project-python
cd my-agent
pip install -e .
```

#### 3. Configure Environment

Create `.env` file:
```bash
LANGSMITH_API_KEY=lsv2_pt_...    # Get free key: smith.langchain.com/settings
OPENAI_API_KEY=sk-...
```

#### 4. Start Server

```bash
langgraph dev
```

Server starts at: **http://localhost:2024**

#### 5. Open Studio UI

Visit: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

You'll see:
- Visual graph representation
- Step-by-step execution
- State inspection
- Interactive testing

### Using Your Server

#### Python SDK (Async)

```python
from langgraph_sdk import get_client
import asyncio

client = get_client(url="http://localhost:2024")

async def main():
    async for chunk in client.runs.stream(
        None,
        "agent",
        input={"messages": [{"role": "human", "content": "Hello!"}]},
    ):
        print(chunk.data)

asyncio.run(main())
```

#### Python SDK (Sync)

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:2024")

for chunk in client.runs.stream(
    None,
    "agent",
    input={"messages": [{"role": "human", "content": "Hello!"}]},
):
    print(chunk.data)
```

#### REST API

```bash
curl --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data '{
        "assistant_id": "agent",
        "input": {"messages": [{"role": "human", "content": "Hello!"}]}
    }'
```

### Persistent Conversations

Use `thread_id` to maintain conversation state:

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:2024")

# First message
client.runs.create(
    thread_id="user-123",
    assistant_id="agent",
    input={"messages": [{"role": "human", "content": "My name is Alice"}]}
)

# Later - remembers context!
response = client.runs.create(
    thread_id="user-123",
    assistant_id="agent",
    input={"messages": [{"role": "human", "content": "What's my name?"}]}
)
# Agent responds: "Your name is Alice"
```

### Important: State vs Context

When building server graphs, understand the difference:

```python
# State = Input/output data (contains messages)
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    response: str

# Context = Configuration parameters (not data)
class Context(TypedDict):
    my_configurable_param: str

# In your node function:
async def call_model(state: State, runtime: Runtime[Context]):
    # ✓ Get messages from state (not runtime.context!)
    messages = state["messages"]

    # ✓ Use ainvoke for async execution (prevents blocking)
    response = await model.ainvoke(messages)
    return {"response": response.content}
```

**Key: Messages go in State, not Context!**

### When to Use Server vs Direct Execution

#### Use Server When:
✅ Visual debugging needed
✅ Testing API integration
✅ Building production apps
✅ Multi-turn conversations
✅ Team collaboration

#### Use Direct Execution When:
✅ Learning basics
✅ Quick prototyping
✅ Writing unit tests
✅ Simple scripts

---

## Key Concepts

### 1. State (Graph API)
Shared data structure with reducers:
```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    count: int
```

### 2. Nodes (Graph API)
Functions that process and update state:
```python
def my_node(state: State):
    return {"messages": [new_message]}
```

### 3. Conditional Edges (Graph API)
Dynamic routing based on state:
```python
def router(state):
    return "continue" if state["count"] < 5 else END

graph.add_conditional_edges("node", router, ["continue", END])
```

### 4. Tasks (Functional API)
Async operations:
```python
@task
def process(data):
    return result
```

### 5. Entrypoint (Functional API)
Main agent logic:
```python
@entrypoint()
def agent(input):
    # Your control flow here
    return output
```

## What You'll Learn

**01_graph_api_basics.py:**
- ✓ Define state with Annotated
- ✓ Build graphs with nodes and edges
- ✓ Implement conditional routing
- ✓ Create agent loops
- ✓ Handle tool execution

**02_functional_api.py:**
- ✓ Use @task and @entrypoint
- ✓ Write agents with Python loops
- ✓ Stream agent execution
- ✓ Simplify agent code

**03_local_server_setup.py:**
- ✓ Run graphs as web API
- ✓ Visual debugging with Studio
- ✓ Persistent conversations
- ✓ Multiple client patterns
- ✓ State vs Context

## Decision Guide

| Feature | Graph API | Functional API | Local Server |
|---------|-----------|----------------|--------------|
| **Complexity** | Complex workflows | Simple agents | Production preview |
| **Code Style** | Declarative | Imperative | Client-server |
| **Control Flow** | Explicit edges | Python loops | API-based |
| **Boilerplate** | More | Less | Setup required |
| **Visualization** | Natural | N/A | Studio UI |
| **Learning Curve** | Steeper | Gentler | Medium |

## Prerequisites

- Python 3.10+ (3.11+ for local server)
- Basic Python knowledge (functions, type hints)
- OpenAI API key
- (Optional) LangSmith API key for local server
- (Recommended) Complete the [LangChain course](../langchain-course/) first

## Resources

- **Official Docs**: https://docs.langchain.com/oss/python/langgraph/quickstart
- **Local Server**: https://docs.langchain.com/oss/python/langgraph/local-server
- **LangGraph GitHub**: https://github.com/langchain-ai/langgraph
- **LangGraph API Docs**: https://langchain-ai.github.io/langgraph/
- **LangSmith**: https://smith.langchain.com/settings

## Tips for Learning

1. **Start with Graph API** - Understand the core concepts
2. **Try Functional API** - See the simpler approach
3. **Test with Server** - Experience production workflow
4. **Experiment** - Modify examples to learn deeply
5. **Read comments** - They explain the "why"

## Troubleshooting

### Import Errors
```bash
pip install --upgrade langgraph langchain-openai
```

### API Key Not Found
Make sure `.env` file exists with `OPENAI_API_KEY=your-key`

### Module Not Found
Activate virtual environment:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### Local Server Issues

**"Module not found" error:**
```bash
cd my-agent
pip install -e .
```

**"LangSmith API key required":**
Get free key: https://smith.langchain.com/settings

**Safari localhost issues:**
```bash
langgraph dev --tunnel
```

**Port already in use:**
```bash
langgraph dev --port 8080
```

## What's Next?

After this course:
- Build stateful AI agents
- Choose the right API for your use case
- Implement complex agent workflows
- Run local server for visual debugging
- Deploy to LangGraph Cloud

**Start with `examples/01_graph_api_basics.py` now!**

## License

MIT License - Feel free to use for learning and teaching.

---

**Total Learning Time**: 1-1.5 hours for all 3 examples

Based on official LangGraph documentation (2025)
