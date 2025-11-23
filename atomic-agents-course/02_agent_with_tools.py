"""
Example 2: Agent with Tools

This example demonstrates how to give an agent access to tools:
- Define custom tools using BaseTool
- Register tools with the agent
- Let the agent decide when to use tools
- Handle tool execution and responses

We'll build a math assistant agent that can perform calculations.
"""

from pydantic import Field
from openai import OpenAI
import instructor
import os
from atomic_agents import AtomicAgent, AgentConfig, BaseIOSchema, BaseTool, BaseToolConfig
from atomic_agents.context import SystemPromptGenerator, ChatHistory, BaseDynamicContextProvider

from dotenv import load_dotenv

load_dotenv()

# Step 1: Define Custom Tools
class CalculatorToolInputSchema(BaseIOSchema):
    """Input for calculator tool"""
    expression: str = Field(..., description="Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')")


class CalculatorToolOutputSchema(BaseIOSchema):
    """Output from calculator tool"""
    result: float = Field(..., description="The calculated result")


class CalculatorToolConfig(BaseToolConfig):
    """Configuration for calculator tool"""
    pass


class CalculatorTool(BaseTool[CalculatorToolInputSchema, CalculatorToolOutputSchema]):
    """A simple calculator tool that can evaluate mathematical expressions"""

    input_schema = CalculatorToolInputSchema
    output_schema = CalculatorToolOutputSchema

    def __init__(self, config: CalculatorToolConfig = CalculatorToolConfig()):
        super().__init__(config)

    def run(self, params: CalculatorToolInputSchema) -> CalculatorToolOutputSchema:
        """Execute the calculator tool"""
        try:
            # Safe evaluation of mathematical expressions
            # In production, use a proper math parser library
            result = eval(params.expression, {"__builtins__": {}}, {})
            return CalculatorToolOutputSchema(result=float(result))
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

class CalculatorProvider(BaseDynamicContextProvider):
    def __init__(self, title):
        super().__init__(title)
        self.result = None

    def get_info(self) -> str:
        return f'CALCULATOR RESULT: "{self.result}"'


calculator_provider = CalculatorProvider("calculator")

# Step 3: Create System Prompt
system_prompt = SystemPromptGenerator(
    background=[
        "You are a helpful math assistant.",
        "You can answer math questions and perform calculations.",
        "You have access to a calculator tool for computations."
    ],
    steps=[
        "Understand the math question",
        "Determine if you need to use the calculator tool",
        "If needed, call the calculator with the appropriate expression",
        "Provide a clear answer with explanation"
    ],
    output_instructions=[
        "Provide the final answer clearly",
        "Explain your reasoning step-by-step",
        "Show any calculations you performed"
    ],
    context_providers={"calculator": calculator_provider}
)


# Step 4: Create the Calculator Tool
calculator_tool = CalculatorTool()

# Step 5: Configure the Agent
# Note: In this simple example, we'll have the agent decide when to use the tool
# and we'll call it manually. For automatic tool calling, you'd use ToolInterfaceAgent
client = instructor.from_openai(OpenAI())

math_agent = AtomicAgent[CalculatorToolInputSchema, CalculatorToolOutputSchema](
    config=AgentConfig(
        client=client,
        model="gpt-4o-mini",
        system_prompt_generator=system_prompt,
        history=ChatHistory(),
    )
)

math_agent.register_context_provider("calculator", calculator_provider)


# Step 6: Use the Tool and Agent Together
if __name__ == "__main__":
    questions = [
        "What is 15 multiplied by 27?",
        "If I have 100 apples and give away 37, then buy 25 more, how many do I have?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}\n")

        # Create input
        input_data = CalculatorToolInputSchema(expression=question)

        # Run agent
        result = math_agent.run(input_data)

        # Display output
        print(f"Answer: {result.result}")
        print("-" * 60 + "\n")
