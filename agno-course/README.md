# Agno AI Framework - Crash Course

A comprehensive crash course on building AI agents with the Agno framework. Learn the essentials in 6 focused lessons.

## What is Agno?

Agno is a Python framework for building multi-agent systems with shared memory, knowledge, and reasoning. It's designed for production use with exceptional performance:

- **529× faster** than LangGraph
- **57× faster** than PydanticAI
- **Agent instantiation:** ~3 microseconds
- **Memory footprint:** ~6.6 KiB per agent

### Why Agno?

1. **Privacy-First**: Runs entirely in your cloud environment
2. **Model-Agnostic**: Works with any LLM provider
3. **Production-Ready**: Includes AgentOS runtime and control plane
4. **Comprehensive Tooling**: 100+ pre-built toolkits with thousands of tools
5. **Enterprise Features**: Human-in-the-loop, guardrails, evaluation framework

## Installation

```bash
# Clone or download this course
cd agno-course

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY=your-key-here
# Optional: export ANTHROPIC_API_KEY=your-key-here
```

## Course Structure

This crash course covers everything you need to get started with Agno in 6 lessons:

### Lesson 1: Basic Agent Fundamentals
**File:** `01_basic_agent.py`

Learn the foundations of creating AI agents with Agno:

- **Minimal Agent**: The simplest possible agent configuration
- **Configured Agent**: Adding instructions, descriptions, and personality
- **Multi-Turn Conversations**: Session memory for context retention

**Key Concepts:**
- The `Agent` class and its core parameters
- `add_history_to_context=True` enables conversation memory
- Instructions guide agent behavior and responses
- Markdown formatting for better output

**Example:**
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["You are a helpful assistant."],
    add_history_to_context=True,
    markdown=True,
)

response = agent.run("Hello!")
print(response.content)
```

### Lesson 2: Agents with Tools
**File:** `02_agents_with_tools.py`

Give your agents superpowers with tools and functions:

- **Built-in Toolkits**: DuckDuckGo for web search, YFinance for financial data
- **Custom Tools**: Turn any Python function into an agent tool
- **Multi-Tool Agents**: Combine multiple tools for comprehensive capabilities

**Key Concepts:**
- Agno includes 100+ pre-built toolkits
- Any Python function with type hints can be a tool
- Docstrings help the LLM understand tool usage
- `debug_mode=True` enables tool call logging for debugging
- Agents intelligently choose which tools to use

**Example:**
```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

def calculate_roi(initial: float, final: float) -> dict:
    """Calculate Return on Investment."""
    profit = final - initial
    roi = (profit / initial) * 100
    return {"roi_percentage": round(roi, 2), "profit": round(profit, 2)}

agent = Agent(
    tools=[
        DuckDuckGoTools(),
        YFinanceTools(),  # Includes all financial data tools
        calculate_roi
    ],
    debug_mode=True  # Shows tool calls in logs
)
```

**Tool Design Best Practices:**
- Use clear, descriptive function names
- Add comprehensive docstrings (Google or NumPy style)
- Use type hints for all parameters and return values
- Return structured data (dicts, Pydantic models)
- Keep functions focused and single-purpose
- Use `debug_mode=True` to see tool calls in action

### Lesson 3: Multi-Agent Teams
**File:** `03_multi_agent_teams.py`

Create teams of specialized agents that collaborate:

- **Research Team**: Web researcher + Financial analyst + Report writer
- **Creative Team**: Strategist + Writer + Editor
- **Specialized Roles**: Each agent has specific expertise and tools

**Key Concepts:**
- `Team` class coordinates multiple agents
- Each agent can have different tools and models
- `role` parameter defines agent specialization
- `show_work=True` reveals collaboration process
- Agents share context and build on each other's work

**Example:**
```python
from agno.team import Team

researcher = Agent(
    name="Researcher",
    role="Research Specialist",
    tools=[DuckDuckGoTools()],
    instructions=["Search for comprehensive information."]
)

analyst = Agent(
    name="Analyst",
    role="Data Analyst",
    tools=[YFinanceTools()],
    instructions=["Analyze financial data."]
)

writer = Agent(
    name="Writer",
    role="Technical Writer",
    instructions=["Synthesize findings into a report."]
)

team = Team(
    name="ResearchTeam",
    agents=[researcher, analyst, writer],
    instructions=["Work together to create comprehensive reports."],
    show_work=True
)

response = team.run("Research Tesla")
```

**Team Design Patterns:**
- **Sequential Pipeline**: Gather → Analyze → Report
- **Parallel Processing**: Multiple specialists working simultaneously
- **Iterative Refinement**: Draft → Review → Improve
- **Hierarchical**: Leader coordinates specialist agents

**Best Practices:**
- Keep teams small (3-5 agents) for clarity
- Define clear roles and responsibilities
- Give each agent appropriate tools for their role
- Use team instructions to coordinate workflow
- Consider computational cost vs. benefit

### Lesson 4: Memory and Storage
**File:** `04_memory_storage.py`

Give agents long-term memory and personalization:

- **Session Memory**: In-memory conversation history (default)
- **Persistent Storage**: SQLite database for cross-session memory
- **User-Specific Memory**: Separate memory per user for multi-user apps

**Key Concepts:**
- `add_history_to_context=True` enables memory
- `SqliteDb` persists conversations to database
- `num_history_runs` controls context window size (default: 3)
- `user_id` parameter for multi-user applications
- `session_id` for explicit session management

**Example:**
```python
from agno.db.sqlite import SqliteDb

# Persistent storage
db = SqliteDb(
    session_table="agent_sessions",
    db_file="agent_memory.db"
)

agent = Agent(
    db=db,
    add_history_to_context=True,
    num_history_runs=5,  # Load last 5 runs
)

# User-specific memory
response1 = agent.run("I love Python", user_id="alice")
response2 = agent.run("What do I love?", user_id="alice")  # Remembers!
```

**Memory Types:**

| Type | Persistence | Use Case |
|------|-------------|----------|
| Session Memory | Single execution | Simple chatbots, demos |
| SqliteDb | Across executions | Production apps, single server |
| PostgresDb | Distributed | Scalable multi-server systems |
| User Memory | Per-user tracking | Multi-tenant applications |

**Configuration Tips:**
- Start with `num_history_runs=3-10` to balance context vs. cost (default is 3)
- Use `SqliteDb` for development and single-server production
- Use `PostgresDb` for distributed, high-scale systems
- Always use `user_id` in multi-user applications
- Consider implementing memory pruning for long conversations

### Lesson 5: Structured Output
**File:** `05_structured_output.py`

Get type-safe, validated responses using Pydantic:

- **Simple Models**: Single entity extraction
- **Nested Structures**: Complex hierarchical data
- **Data Validation**: Automatic validation with Pydantic
- **Production Integration**: Direct database/API integration

**Key Concepts:**
- `response_model` parameter accepts Pydantic models
- Field descriptions guide the LLM
- Automatic type validation and error handling
- Support for nested models and lists
- Validation constraints (min, max, ge, le, etc.)

**Example:**
```python
from pydantic import BaseModel, Field
from typing import List

class MovieRecommendation(BaseModel):
    title: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Primary genre")
    year: int = Field(..., description="Release year")
    rating: float = Field(..., ge=0, le=10, description="Rating out of 10")
    reason: str = Field(..., description="Why this movie is recommended")

agent = Agent(
    response_model=MovieRecommendation
)

movie = agent.run("Recommend a sci-fi movie")
print(f"{movie.title} ({movie.year}) - {movie.rating}/10")
```

**Benefits:**
- ✅ Type-safe responses you can trust
- ✅ Automatic validation and error handling
- ✅ Easy database and API integration
- ✅ Self-documenting code
- ✅ IDE autocomplete support

**Best Practices:**
- Use clear, descriptive field names
- Add Field descriptions for better LLM guidance
- Set appropriate validation constraints
- Use `Optional[Type]` for nullable fields
- Create reusable model components
- Document complex models with examples

**Common Use Cases:**
- API response formatting
- Database record creation
- Form data processing
- Data extraction from text
- Report generation
- Configuration parsing
- Analytics results

### Lesson 6: AgentOS Deployment
**File:** `06_agentos_fastapi.py`

Deploy your agents as production web services with AgentOS:

- **AgentOS Runtime**: Production-ready agent hosting with FastAPI
- **Automatic API Generation**: RESTful endpoints for agents, teams, and workflows
- **Built-in Management**: Sessions, memory, metrics, and monitoring
- **Multi-User Support**: User-specific sessions and memory

**Key Concepts:**
- `AgentOS` wraps agents/teams as web services
- Automatic OpenAPI documentation at `/docs`
- Built-in endpoints for sessions, memory, metrics
- Database auto-provisioning and management
- Hot reload during development

**Example:**
```python
from agno.os import AgentOS
from agno.agent import Agent
from agno.db.sqlite import SqliteDb

agent = Agent(
    name="Assistant",
    agent_id="assistant",
    db=SqliteDb(session_table="sessions", db_file="agent.db"),
    add_history_to_context=True
)

# Create AgentOS with the agent
agent_os = AgentOS(
    name="MyAssistantOS",
    agents=[agent],
    description="A helpful AI assistant service"
)

# Get the FastAPI app
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(
        app="06_agentos_fastapi:app",
        host="0.0.0.0",
        port=7777,  # Default AgentOS port
        reload=True
    )
```

**Running the Server:**
```bash
python 06_agentos_fastapi.py
```

**Built-in API Endpoints:**

AgentOS automatically generates RESTful endpoints for all your agents, teams, and workflows:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/docs` | GET | Interactive OpenAPI documentation |
| `/redoc` | GET | Alternative API documentation |
| `/health` | GET | Service health check |
| `/agents/{agent_id}/run` | POST | Execute an agent |
| `/teams/{team_id}/run` | POST | Execute a team |
| `/workflows/{workflow_id}/run` | POST | Execute a workflow |
| `/sessions` | GET | List all sessions |
| `/sessions/{id}` | GET | Get specific session |
| `/memory` | GET | Get user memories |
| `/metrics` | GET | Get performance metrics |

All endpoints support filtering by `user_id`, `session_id`, and other parameters.

**Using the API:**

```bash
# Health check
curl http://localhost:7777/health

# Run an agent (creates new session)
curl -X POST http://localhost:7777/agents/SimpleAssistant/run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is AI?",
    "user_id": "alice"
  }'

# Continue conversation (use returned session_id)
curl -X POST http://localhost:7777/agents/SimpleAssistant/run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more",
    "session_id": "abc-123",
    "user_id": "alice"
  }'

# Run a team
curl -X POST http://localhost:7777/teams/ResearchTeam/run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Research Tesla stock and recent news"
  }'

# Get all sessions for a user
curl "http://localhost:7777/sessions?user_id=alice"

# Get specific session details
curl "http://localhost:7777/sessions/abc-123"

# Get user memory
curl "http://localhost:7777/memory?user_id=alice"

# Get agent performance metrics
curl "http://localhost:7777/metrics?agent_id=SimpleAssistant"
```

**Python Client Example:**

```python
import requests

BASE_URL = "http://localhost:7777"

# Start a conversation
response = requests.post(
    f"{BASE_URL}/agents/ResearchAssistant/run",
    json={
        "message": "What is the current price of AAPL?",
        "user_id": "alice"
    }
)

result = response.json()
print(f"Response: {result['content']}")
session_id = result['session_id']  # Save for next message

# Continue the conversation
response = requests.post(
    f"{BASE_URL}/agents/ResearchAssistant/run",
    json={
        "message": "What about Tesla?",
        "session_id": session_id,  # Same session
        "user_id": "alice"
    }
)
print(f"Response: {response.json()['content']}")

# Get all sessions for this user
sessions = requests.get(
    f"{BASE_URL}/sessions",
    params={"user_id": "alice"}
).json()

print(f"User has {len(sessions)} sessions")

# Get agent metrics
metrics = requests.get(
    f"{BASE_URL}/metrics",
    params={"agent_id": "ResearchAssistant"}
).json()

print(f"Agent metrics: {metrics}")
```

**Production Deployment Checklist:**

1. **Database**: Switch from SQLite to PostgreSQL
   ```python
   from agno.db.postgres import PostgresDb
   
   db = PostgresDb(
       host="localhost",
       port=5432,
       user="agno_user",
       password="secure_password",
       database="agno_prod",
       session_table="sessions"
   )
   ```

2. **Environment Variables**: Use `.env` file or environment variables
   ```bash
   export OPENAI_API_KEY="sk-..."
   export AGNO_DB_HOST="prod-db.example.com"
   export AGNO_DB_PASSWORD="..."
   ```

3. **Production Server**: Use gunicorn with uvicorn workers
   ```bash
   pip install gunicorn
   
   gunicorn 06_agentos_fastapi:app \
     --workers 4 \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:7777 \
     --timeout 120 \
     --access-logfile logs/access.log \
     --error-logfile logs/error.log
   ```

4. **Security**:
   - Enable API key authentication
   - Configure CORS for your domain
   - Use HTTPS with proper SSL certificates
   - Implement rate limiting

5. **Monitoring**:
   - Set up logging aggregation (ELK, CloudWatch, etc.)
   - Monitor metrics endpoints
   - Set up health check alerts
   - Track database performance

6. **Scaling**:
   - Use load balancers (AWS ALB, nginx, etc.)
   - Scale horizontally with multiple workers
   - Use connection pooling for database
   - Consider caching layer (Redis) for sessions

**AgentOS Features:**
- ✅ Automatic API generation for agents/teams/workflows
- ✅ Built-in database management and auto-provisioning
- ✅ Session tracking and management
- ✅ User memory across sessions
- ✅ Performance metrics and monitoring
- ✅ WebSocket support for streaming
- ✅ Stateless design for horizontal scaling
- ✅ Async by default for high performance

## Running the Examples

Each file is standalone and can be run independently:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run lessons in order
python 01_basic_agent.py
python 02_agents_with_tools.py
python 03_multi_agent_teams.py
python 04_memory_storage.py
python 05_structured_output.py

# Run the FastAPI server
python 06_agentos_fastapi.py
```

## Next Steps

After completing this crash course, you can:

1. **Explore Advanced Features:**
   - RAG (Retrieval Augmented Generation) with vector databases
   - Reasoning agents with chain-of-thought
   - Workflows with deterministic state machines
   - Custom model providers and adapters

2. **Build Production Applications:**
   - Deploy with AgentOS control plane
   - Scale with Kubernetes
   - Integrate with your existing systems
   - Add authentication and rate limiting

3. **Join the Community:**
   - GitHub: https://github.com/agno-agi/agno
   - Documentation: https://docs.agno.com
   - Discord: Get help and share your projects
   - Examples: Check out cookbook recipes

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Application                        │
├─────────────────────────────────────────────────────────────┤
│                   Agno Framework                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Agents  │  │  Teams   │  │ Workflows│  │ Memory   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Tools   │  │ Knowledge│  │ Storage  │  │ Models   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    AgentOS Runtime                          │
│  (FastAPI Server + Control Plane)                          │
└─────────────────────────────────────────────────────────────┘
```

## Key Takeaways

1. **Agents are the building blocks** - Start simple, add complexity as needed
2. **Tools extend capabilities** - 100+ toolkits available, easy to create custom ones
3. **Teams enable specialization** - Divide complex tasks among expert agents
4. **Memory enables personalization** - Remember context and user preferences
5. **Structured output ensures reliability** - Type-safe responses for production
6. **AgentOS makes deployment easy** - Production-ready FastAPI integration

## Best Practices Summary

### Agent Design
- Start with clear instructions
- Add tools only when needed
- Use appropriate model for the task
- Enable memory for conversational agents
- Test with diverse inputs

### Tool Development
- Clear function names and docstrings
- Type hints on all parameters
- Return structured data
- Handle errors gracefully
- Keep functions focused

### Team Architecture
- 3-5 agents per team (optimal)
- Clear role definition
- Appropriate tools per role
- Well-defined coordination strategy
- Monitor computational cost

### Memory Management
- Use session memory for simple apps
- SQLite for single-server production
- PostgreSQL for distributed systems
- Configure `num_history_responses` appropriately
- Implement user_id for multi-tenant apps

### Production Deployment
- Use persistent storage (not in-memory)
- Implement proper error handling
- Add authentication and rate limiting
- Monitor performance and costs
- Version your agents and APIs
- Use environment variables for config

## Resources

- **Official Documentation**: https://docs.agno.com
- **GitHub Repository**: https://github.com/agno-agi/agno
- **Example Cookbook**: https://docs.agno.com/examples
- **API Reference**: https://docs.agno.com/api
- **Community Forum**: Discourse and Discord

## License

This course is for educational purposes. Agno framework is licensed under Apache 2.0.

---

**Happy Building! 🚀**

Start with Lesson 1 and progress through each lesson. By the end, you'll have a solid understanding of building production-ready AI agents with Agno.
