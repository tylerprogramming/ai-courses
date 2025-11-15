import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

CREW_URL = os.environ.get("CREW_URL")
CREW_TOKEN = os.environ.get("CREW_TOKEN")

print("=== Debug CrewAI Kickoff ===\n")
print(f"CREW_URL: {CREW_URL}")
print(f"CREW_TOKEN: {CREW_TOKEN[:20]}..." if CREW_TOKEN else "CREW_TOKEN: None")
print()

# Test inputs
inputs = {
    "slack_channel": "#ai",
    "idea": "AI Agent Frameworks",
    "target_audience": "AI enthusiasts",
    "tone": "formal",
    "examples_document_url": "https://docs.google.com/document/d/1cQiOcpc739F_cEwl9gmUe6KumiSbmYTDKGf3ZYnWdyQ/edit?tab=t.0"
}

# Prepare request
url = f"{CREW_URL.rstrip('/')}/kickoff"
headers = {
    "Authorization": f"Bearer {CREW_TOKEN}",
    "Content-Type": "application/json"
}
payload = {"inputs": inputs}

print("Request URL:")
print(f"  {url}\n")

print("Request Headers:")
print(f"  Authorization: Bearer {CREW_TOKEN[:20]}...")
print(f"  Content-Type: application/json\n")

print("Request Payload:")
print(json.dumps(payload, indent=2))
print()

# Send request
print("Sending request...\n")
response = requests.post(url, json=payload, headers=headers)

print(f"Response Status: {response.status_code}")
print()

print("Response Headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")
print()

print("Response Body:")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
