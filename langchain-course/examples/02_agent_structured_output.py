from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.agents.structured_output import ToolStrategy
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    response_format=ToolStrategy(ResponseFormat)
)

# Run the agent
response =agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response['structured_response'])