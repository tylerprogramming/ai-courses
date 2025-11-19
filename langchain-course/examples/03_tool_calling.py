"""
Topic 3: Tool Calling (Function Calling)

Tool calling allows LLMs to generate structured outputs and interact
with external systems (APIs, databases, functions).
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()


# Define tools using @tool decorator
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: City and state, e.g., 'San Francisco, CA'
    """
    # Mock weather data (in real app, call weather API)
    return f"The weather in {location} is sunny and 72°F"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Math expression like '2 + 2' or '10 * 5'
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# Example: Basic Tool Calling
# ============================================================================

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_weather, calculate]

# Bind tools to model
model_with_tools = model.bind_tools(tools)

print("Example: Tool Calling")
print("-" * 60)
question = "What's the weather in Boston and what is 25 * 4?"
print(f"Question: {question}\n")

response = model_with_tools.invoke([HumanMessage(content=question)])

# Execute tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool called: {tool_call['name']}")
        print(f"Arguments: {tool_call['args']}")

        # Execute the tool
        if tool_call['name'] == 'get_weather':
            result = get_weather.invoke(tool_call['args'])
        elif tool_call['name'] == 'calculate':
            result = calculate.invoke(tool_call['args'])

        print(f"Result: {result}\n")

print("✓ Tools enable LLMs to interact with external systems")
print("✓ Next: 04_prompts_templates.py")
