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
    def __init__(self, title: str, calculation_result: CalculatorToolOutputSchema | Exception | None = None):
        super().__init__(title=title)
        self.calculation_result = calculation_result

    def get_info(self) -> str:
        if self.calculation_result is None:
            return f"{self.title}: No calculation performed yet"
        return f"{self.title}: {self.calculation_result}"


# Step 3: Define Agent Input/Output Schemas (separate from tool schemas)
class MathAgentInputSchema(BaseIOSchema):
    """Input schema for the math agent"""
    question: str = Field(..., description="Math question from the user")


class MathAgentOutputSchema(BaseIOSchema):
    """Output schema for the math agent"""
    answer: str = Field(..., description="Answer to the user's math question")
    expression_used: str | None = Field(None, description="The mathematical expression that was evaluated, if any")


# Step 4: Create System Prompt
system_prompt = SystemPromptGenerator(
    background=[
        "You are a helpful math assistant.",
        "You can answer math questions and perform calculations.",
        "You have access to calculator results for computations."
    ],
    steps=[
        "Understand the math question",
        "Use the calculator results provided in context",
        "Provide a clear answer with explanation"
    ],
    output_instructions=[
        "Provide the final answer clearly",
        "Explain your reasoning step-by-step",
        "Show any calculations you performed"
    ]
)


# Step 5: Create the Calculator Tool
calculator_tool = CalculatorTool()

# Step 6: Configure the Agent
client = instructor.from_openai(OpenAI())

math_agent = AtomicAgent[MathAgentInputSchema, MathAgentOutputSchema](
    config=AgentConfig(
        client=client,
        model="gpt-4o-mini",
        system_prompt_generator=system_prompt,
        history=ChatHistory(),
    )
)


# Step 7: Use the Tool and Agent Together
if __name__ == "__main__":
    # Example math problems with their expressions
    problems = [
        {
            "question": "What is 15 multiplied by 27?",
            "expression": "15 * 27"
        },
        {
            "question": "If I have 100 apples and give away 37, then buy 25 more, how many do I have?",
            "expression": "100 - 37 + 25"
        },
    ]

    for i, problem in enumerate(problems, 1):
        print(f"Question {i}: {problem['question']}\n")

        # Step 1: Run the calculator tool first
        calculator_input = CalculatorToolInputSchema(expression=problem['expression'])
        
        try:
            calculator_result = calculator_tool.run(calculator_input)
            calculator_provider = CalculatorProvider("Calculator Result", calculator_result)
            print(f"Calculator computed: {problem['expression']} = {calculator_result.result}")
        except Exception as e:
            calculator_provider = CalculatorProvider("Calculator Failed", e)
            print(f"Calculator error: {e}")
        
        # Step 2: Register the calculator results as context for the agent
        math_agent.register_context_provider("calculator", calculator_provider)

        # Step 3: Run the agent with the natural language question
        agent_input = MathAgentInputSchema(question=problem['question'])
        answer = math_agent.run(agent_input)

        # Display output
        print(f"Agent Answer: {answer.answer}")
        if answer.expression_used:
            print(f"Expression Used: {answer.expression_used}")
        print("-" * 60 + "\n")
