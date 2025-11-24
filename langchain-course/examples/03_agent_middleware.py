from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.tools import tool
from langchain.agents.structured_output import ToolStrategy
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    result: str
    expression: str | None = None

@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

agent = create_agent(
    model="gpt-4o",
    tools=[calc],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            max_tokens_before_summary = 250,
            messages_to_keep = 10,
        ),
    ],
    response_format=ToolStrategy(ResponseFormat)
)

response = agent.invoke({"messages": [{"role": "user", "content": "What is 100 * 100?"}]})
print(response['structured_response'])