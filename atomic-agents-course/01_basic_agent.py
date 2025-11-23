"""
Example 1: Basic Atomic Agent

This example demonstrates the fundamental structure of an Atomic Agent:
- Input schema (Pydantic model)
- Output schema (Pydantic model)
- Agent configuration
- System prompt
- Agent execution

We'll build a simple sentiment analysis agent.
"""

from pydantic import Field
from openai import OpenAI
import instructor
from atomic_agents import AtomicAgent, AgentConfig, BaseIOSchema
from atomic_agents.context import SystemPromptGenerator, ChatHistory

from dotenv import load_dotenv

load_dotenv()

# Step 1: Define Input Schema
class SentimentInput(BaseIOSchema):
    """Input schema for sentiment analysis"""
    text: str = Field(..., description="The text to analyze for sentiment")


# Step 2: Define Output Schema
class SentimentOutput(BaseIOSchema):
    """Output schema for sentiment analysis results"""
    sentiment: str = Field(..., description="The detected sentiment: positive, negative, or neutral")
    confidence: float = Field(..., description="Confidence score between 0 and 1", ge=0, le=1)
    reasoning: str = Field(..., description="Brief explanation of the sentiment analysis")


# Step 3: Create System Prompt
system_prompt = SystemPromptGenerator(
    background=[
        "You are a sentiment analysis expert.",
        "You analyze text and determine its emotional tone."
    ],
    steps=[
        "Read the provided text carefully",
        "Identify the overall emotional tone (positive, negative, or neutral)",
        "Assess your confidence in the analysis",
        "Provide a brief reasoning for your conclusion"
    ],
    output_instructions=[
        "Return sentiment as: 'positive', 'negative', or 'neutral'",
        "Confidence should be between 0 and 1",
        "Reasoning should be concise (1-2 sentences)"
    ]
)


# Step 4: Configure the Agent
client = instructor.from_openai(OpenAI())

# Initialize the agent
agent = AtomicAgent[SentimentInput, SentimentOutput](
    config=AgentConfig(
        client=client,
        model="gpt-4o-mini",
        system_prompt_generator=system_prompt,
        history=ChatHistory(),
    )
)


# Step 5: Use the Agent
if __name__ == "__main__":
    print("=== Atomic Agents: Basic Agent Example ===\n")

    # Test cases
    test_texts = [
        "I absolutely love this product! It exceeded all my expectations.",
        "This is the worst experience I've ever had. Completely disappointed.",
        "The weather today is cloudy with a chance of rain.",
    ]

    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: {text}\n")

        # Create input
        input_data = SentimentInput(text=text)

        # Run agent
        result = agent.run(input_data)

        # Display output
        print(f"Sentiment: {result.sentiment}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")
        print("-" * 60 + "\n")
