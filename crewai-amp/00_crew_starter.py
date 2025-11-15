from crewai_client import CrewAIClient

# Initialize client (uses CREW_URL and CREW_TOKEN from .env)
client = CrewAIClient()

# Step 1: Get required inputs
print("Step 1: Getting required inputs...")
required_inputs = client.get_inputs()
print(f"Required inputs: {required_inputs}\n")

# Step 2: Prepare inputs
# Replace these with your actual input values
inputs = {
    "slack_channel": "#ai",
    "idea": "AI Agent Frameworks",
    "target_audience": "AI enthusiasts",
    "tone": "formal",
    "examples_document_url": "https://docs.google.com/document/d/1cQiOcpc739F_cEwl9gmUe6KumiSbmYTDKGf3ZYnWdyQ/edit?tab=t.0"
}

print(f"Step 2: Preparing inputs:")
print(f"Inputs: {inputs}\n")

# Step 3: Kickoff execution and wait for completion
print("Step 3: Starting crew execution...")


def on_status(status):
    """Callback for status updates."""
    state = status.get("status", status.get("state", "unknown"))
    print(f"  Status: {state}")


result = client.kickoff_and_wait(
    inputs=inputs,
    poll_interval=15,
    callback=on_status
)

# Step 4: Display results
print("\n✓ Execution completed!")
print("\nFinal result:")
print(result)
