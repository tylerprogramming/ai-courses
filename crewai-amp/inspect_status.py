import sys
import json
from crewai_client import CrewAIClient

if len(sys.argv) < 2:
    print("Usage: python inspect_status.py <kickoff_id>")
    sys.exit(1)

kickoff_id = sys.argv[1]

client = CrewAIClient()

print(f"Fetching status for kickoff_id: {kickoff_id}\n")

status = client.get_status(kickoff_id)

print("=== Full Status Response ===")
print(json.dumps(status, indent=2))

print("\n=== Key Fields ===")
print(f"status field: {status.get('status')}")
print(f"state field: {status.get('state')}")
print(f"result field: {status.get('result')}")
print(f"error field: {status.get('error')}")

print("\n=== All Keys ===")
for key in status.keys():
    print(f"  {key}: {type(status[key]).__name__}")
