import instructor
import openai
from pydantic import Field
from atomic_agents import BaseIOSchema, AtomicAgent, AgentConfig
from atomic_agents.context import SystemPromptGenerator

# Import the search tool you want to use
from web_search_agent.tools.searxng_search import SearXNGSearchTool

# Define the input schema for the query agent
class QueryAgentInputSchema(BaseIOSchema):
    """Input schema for the QueryAgent."""
    instruction: str = Field(..., description="Instruction to generate search queries for.")
    num_queries: int = Field(..., description="Number of queries to generate.")

# Initialize the query agent
query_agent = AtomicAgent[QueryAgentInputSchema, SearXNGSearchTool.input_schema](
    config=AgentConfig(
        client=instructor.from_openai(openai.OpenAI()),
        model="gpt-5-mini",
        system_prompt_generator=SystemPromptGenerator(
            background=[
                "You are an intelligent query generation expert.",
                "Your task is to generate a specified number of diverse and highly relevant queries based on a given instruction."
            ],
            steps=[
                "Receive the instruction and the number of queries to generate.",
                "Generate the queries in JSON format."
            ],
            output_instructions=[
                "Ensure each query is unique and relevant.",
                "Provide the queries in the expected schema."
            ],
        ),
    )
)

# Import a different search tool
from web_search_agent.tools.some_search_tool import SomeSearchTool

# Update the output schema
query_agent.config.output_schema = SomeSearchTool.input_schema