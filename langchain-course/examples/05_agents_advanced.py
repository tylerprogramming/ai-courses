"""
Example 5: Agents - Advanced Patterns

Learn how to:
- Use context with agents
- Implement structured output in agents
- Combine multiple capabilities
- Build production-ready agent systems

Based on: https://docs.langchain.com/oss/python/langchain/quickstart
"""

import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field

load_dotenv()


# ============================================================================
# 1. Define Context Schema
# ============================================================================

class Context(TypedDict):
    """Runtime context for the agent"""
    user_id: str
    session_id: str

# ============================================================================
# 2. Define Tools with Context Access
# ============================================================================

@tool
def get_user_location(user_id: str) -> str:
    """Get the user's location from their profile.

    Args:
        user_id: The user's ID
    """
    locations = {
        "user_123": "San Francisco, CA",
        "user_456": "New York, NY"
    }
    return locations.get(user_id, "Location unknown")


@tool
def get_weather_for_location(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: City and state, e.g. San Francisco, CA
    """
    weather = {
        "san francisco, ca": "Sunny, 72°F",
        "new york, ny": "Cloudy, 65°F"
    }
    return weather.get(location.lower(), "Weather data unavailable")


@tool
def create_recommendation(user_id: str, recommendation: str) -> str:
    """Create a personalized recommendation for a user.

    Args:
        user_id: The user's ID
        recommendation: The recommendation text
    """
    return f"Recommendation saved for {user_id}: {recommendation}"


tools = [get_user_location, get_weather_for_location, create_recommendation]

# ============================================================================
# 3. Define Structured Output
# ============================================================================

class ResponseFormat(BaseModel):
    """Structured response format"""
    summary: str = Field(description="Brief summary of the interaction")
    action_taken: str = Field(description="What action was performed")
    follow_up_needed: bool = Field(description="Whether follow-up is needed")


# ============================================================================
# 4. Create Advanced Agent
# ============================================================================

model = init_chat_model("gpt-4o-mini", temperature=0)

system_prompt = """You are a personalized weather assistant.

You can:
- Look up user locations
- Get weather information
- Create personalized recommendations

Always provide helpful, context-aware responses based on the user's information."""

checkpointer = MemorySaver()

# Note: Structured output with agents requires additional configuration
# For this example, we'll demonstrate the basic pattern
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=checkpointer
)

# ============================================================================
# 5. Run Agent with Context
# ============================================================================

# Context provides user-specific information
context = Context(user_id="user_123", session_id="session_001")

config = {"configurable": {"thread_id": "advanced_thread"}}

# First query
print("\nUser: What's the weather where I am?")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather where I am? My user ID is user_123"}]},
    config=config
)
print(f"Agent: {result['messages'][-1].content}")

# Follow-up using memory
print("\nUser: Should I bring an umbrella?")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Should I bring an umbrella?"}]},
    config=config
)
print(f"Agent: {result['messages'][-1].content}")


# ============================================================================
# 6. Multi-tool Workflow
# ============================================================================

complex_query = """I'm user_456. Can you:
1. Check my location
2. Get the weather there
3. Give me a recommendation for what to wear today"""

print(f"User: {complex_query}")

result = agent.invoke(
    {"messages": [{"role": "user", "content": complex_query}]},
    config={"configurable": {"thread_id": "workflow_thread"}}
)

print(f"\nAgent: {result['messages'][-1].content}")
