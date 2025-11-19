"""
Example 3: Agents - Basic Usage

Learn how to:
- Create agents with create_agent()
- Define tools for agents
- Run agent conversations
- Handle agent responses

Based on: https://docs.langchain.com/oss/python/langchain/agents
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()


# ============================================================================
# 1. Define Agent Tools
# ============================================================================

@tool
def search_database(query: str) -> str:
    """Search a database for information.

    Args:
        query: The search query
    """
    # Simulated database
    database = {
        "product pricing": "Our products range from $99/month (Basic) to $499/month (Enterprise)",
        "support hours": "24/7 email support, phone support Mon-Fri 9am-5pm PST",
        "company founded": "Founded in 2010 by Jane Smith and John Doe"
    }

    for key in database:
        if key in query.lower():
            return database[key]

    return "No information found. Try searching for: product pricing, support hours, or company founded"


@tool
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the final price after applying a discount.

    Args:
        price: Original price
        discount_percent: Discount percentage (e.g., 20 for 20%)
    """
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return round(final_price, 2)


tools = [search_database, calculate_discount]


# ============================================================================
# 2. Create Agent with create_agent
# ============================================================================

# Initialize model
model = init_chat_model("gpt-4o-mini", temperature=0)

# System prompt defines agent behavior
system_prompt = """You are a helpful customer service assistant.

You have access to tools to:
1. Search the company database for information
2. Calculate discounts

Always think step-by-step and use the available tools when needed."""

# Create agent using create_agent (builds a graph-based agent with LangGraph)
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)


# ============================================================================
# 3. Single Agent Invocation
# ============================================================================

result = agent.invoke(
    {"messages": [{"role": "user", "content": "When was your company founded?"}]}
)

print(f"User: When was your company founded?")
print(f"Agent: {result['messages'][-1].content}\n")


# ============================================================================
# 4. Multi-step Reasoning
# ============================================================================

questions = [
    "What is your enterprise pricing?",
    "If I get a 15% discount, what would the enterprise price be?",
]

for question in questions:
    print(f"\nUser: {question}")

    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    answer = result['messages'][-1].content
    print(f"Agent: {answer}")
