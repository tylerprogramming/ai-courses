from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
)
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# 1. Define the guardrail output model
class ContentModerationOutput(BaseModel):
    reasoning: str
    is_inappropriate: bool


# 2. Create a guardrail agent to check for inappropriate content
guardrail_agent = Agent(
    name="Content Moderator",
    instructions="""Check if the user's message contains inappropriate content,
    spam, or requests that violate community guidelines. Consider:
    - Abusive or offensive language
    - Spam or promotional content
    - Requests for harmful information
    Return is_inappropriate=True if any issues are found.""",
    output_type=ContentModerationOutput,
)


# 3. Create the guardrail function
@input_guardrail
async def content_guardrail(
    context: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    """
    Input guardrail that checks for inappropriate content before processing.
    Runs in parallel with the main agent execution.
    """
    result = await Runner.run(guardrail_agent, input, context=context.context)
    final_output = result.final_output_as(ContentModerationOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_inappropriate,
    )


# 4. Define language-specific agents
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

# 5. Create triage agent with guardrails
triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    input_guardrails=[content_guardrail],  # Add guardrail here
)


async def main():
    # # Interactive loop to demonstrate guardrails
    input_data: list[TResponseInputItem] = []

    while True:
        try:
            user_input = input("You: ")
            input_data.append({"role": "user", "content": user_input})

            result = await Runner.run(triage_agent, input_data)
            print(f"Agent: {result.final_output}\n")
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered:
            refusal_message = "I'm sorry, but I cannot process that request due to content policy violations."
            print(f"Agent: {refusal_message}\n")
            input_data.append({"role": "assistant", "content": refusal_message})
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    asyncio.run(main())