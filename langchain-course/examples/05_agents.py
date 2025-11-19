"""
Topic 5: Agents (ReAct Framework)

Agents use LLMs to reason about what to do, execute actions,
and continue until the task is complete.

ReAct = Reasoning + Acting (recommended approach in 2025)
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate

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

# ReAct prompt template
react_prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

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

Question: {input}
Thought: {agent_scratchpad}
""")

# Create ReAct agent
agent = create_react_agent(llm, tools, react_prompt)

# Create agent executor (handles the execution loop)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Shows reasoning steps
    handle_parsing_errors=True,
    max_iterations=5
)

print("Example: ReAct Agent")
print("=" * 60)

question = "What is the length of the word 'LangChain' multiplied by 2?"
print(f"Question: {question}\n")

result = agent_executor.invoke({"input": question})

print("\n" + "=" * 60)
print(f"Final Answer: {result['output']}")

print("\n✓ Agents reason and act dynamically")
print("✓ Use create_react_agent() (modern approach)")
print("✓ For complex multi-agent systems, use LangGraph")
print("✓ Next: 06_memory.py")
