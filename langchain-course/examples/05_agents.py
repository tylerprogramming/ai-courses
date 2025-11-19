"""
Topic 5: Agents (ReAct Framework)

Agents use LLMs to reason about what to do, execute actions,
and continue until the task is complete.

ReAct = Reasoning + Acting
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()


# Define tools for the agent
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


# ============================================================================
# Example: ReAct Agent
# ============================================================================

llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Use GPT-4 for better reasoning
tools = [get_word_length, multiply]

# System prompt for the agent (simple string, not a template)
system_prompt = """You are a helpful assistant that can use tools to answer questions.
Think step by step and use the available tools when needed.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""

# Create agent using the modern create_agent function
agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

print("Example: Agent with Tools")
print("=" * 60)

question = "What is the length of the word 'LangChain' multiplied by 2?"
print(f"Question: {question}\n")

result = agent.invoke({"messages": [("user", question)]})

print("\n" + "=" * 60)
print(f"Final Answer: {result['messages'][-1].content}")
