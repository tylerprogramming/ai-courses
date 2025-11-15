# CrewAI AMP API Client

Python client and tools for interacting with CrewAI AMP deployed crews.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```bash
cp .env.example .env
```

Then edit `.env` and add your credentials:
```bash
CREW_URL=https://your-crew-url.crewai.com
CREW_TOKEN=your_crew_token_here
```

## Project Files

### crewai_client.py
Core Python client library for CrewAI AMP API.

**Key Methods:**
- `get_inputs()` - Get required input parameters
- `kickoff(inputs)` - Start crew execution
- `get_status(kickoff_id)` - Check execution status
- `wait_for_completion(kickoff_id)` - Poll until completion
- `kickoff_and_wait(inputs)` - Kickoff and wait in one call

**Example:**
```python
from crewai_client import CrewAIClient

client = CrewAIClient()

# Get required inputs
inputs_list = client.get_inputs()

# Kickoff and wait
result = client.kickoff_and_wait({
    "topic": "AI Agent Frameworks",
    "current_year": "2025"
})
```

### 00_crew_starter.py
Simple starter script showing basic usage.

**Run:**
```bash
python 00_crew_starter.py
```

Edit the `inputs` dictionary in the file to match your crew's required inputs.

### 01_crew_cli.py
Interactive command-line tool for managing crew executions.

**Commands:**
```bash
# Get required inputs
python 01_crew_cli.py inputs

# Start execution (interactive prompts)
python 01_crew_cli.py kickoff

# Check status
python 01_crew_cli.py status <kickoff_id>

# Run and wait for completion (interactive)
python 01_crew_cli.py run

# Wait for existing execution
python 01_crew_cli.py wait <kickoff_id>
```

**Features:**
- Interactive input collection
- Real-time status updates
- JSON formatted output
- Error handling

### 02_crew_api.py
FastAPI server providing a REST API wrapper around CrewAI AMP.

**Start server:**
```bash
python 02_crew_api.py
# or
uvicorn 02_crew_api:app --reload --port 8001
```

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/inputs` | Get required inputs |
| POST | `/kickoff` | Start execution |
| GET | `/status/{kickoff_id}` | Get execution status |
| GET | `/executions` | List all tracked executions |
| DELETE | `/executions/{kickoff_id}` | Delete execution tracking |
| DELETE | `/executions` | Clear all executions |

**Interactive docs:** http://localhost:8001/docs

**Example API Calls:**

```bash
# Get required inputs
curl http://localhost:8001/inputs

# Kickoff execution (async)
curl -X POST http://localhost:8001/kickoff \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "topic": "AI Agent Frameworks",
      "current_year": "2025"
    },
    "wait": false
  }'

# Kickoff and wait (sync)
curl -X POST http://localhost:8001/kickoff \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "topic": "AI Agent Frameworks",
      "current_year": "2025"
    },
    "wait": true
  }'

# Get status
curl http://localhost:8001/status/{kickoff_id}

# List all executions
curl http://localhost:8001/executions
```

## CrewAI AMP API Reference

### 1. Get Required Inputs
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  https://your-crew-url.crewai.com/inputs
```

**Response:**
```json
{"inputs":["topic","current_year"]}
```

### 2. Kickoff Execution
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  -d '{"inputs": {"topic": "AI", "current_year": "2025"}}' \
  https://your-crew-url.crewai.com/kickoff
```

**Response:**
```json
{"kickoff_id":"abcd1234-5678-90ef-ghij-klmnopqrstuv"}
```

### 3. Check Status
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  https://your-crew-url.crewai.com/status/{kickoff_id}
```

## Usage Patterns

### Pattern 1: Fire and Forget
```python
client = CrewAIClient()
kickoff_id = client.kickoff({"topic": "AI", "current_year": "2025"})
print(f"Started: {kickoff_id}")
# Check status later
```

### Pattern 2: Wait for Completion
```python
client = CrewAIClient()
result = client.kickoff_and_wait(
    {"topic": "AI", "current_year": "2025"},
    poll_interval=5
)
print(result)
```

### Pattern 3: Custom Status Callback
```python
def on_status(status):
    state = status.get("status", "unknown")
    print(f"Current state: {state}")

client = CrewAIClient()
result = client.kickoff_and_wait(
    {"topic": "AI", "current_year": "2025"},
    callback=on_status
)
```

### Pattern 4: With Timeout
```python
client = CrewAIClient()
try:
    result = client.kickoff_and_wait(
        {"topic": "AI", "current_year": "2025"},
        timeout=300  # 5 minutes
    )
except TimeoutError:
    print("Execution timed out")
```

## Debugging

### Check Crew Logs
1. Go to CrewAI AMP dashboard
2. Navigate to "Executions" tab
3. Find your execution by kickoff_id
4. View detailed logs and traces

### Common Issues

**Authentication Error:**
- Verify `CREW_TOKEN` is correct
- Ensure token has not expired

**Input Validation Error:**
- Use `get_inputs()` to confirm required parameters
- Check input types match expected format

**Timeout:**
- Increase `timeout` parameter
- Check crew execution logs for stuck tasks

## Advanced Features

### Background Execution Tracking (API)
The FastAPI server tracks executions in memory:
- Automatic status polling in background
- View all executions via `/executions`
- Results cached locally

**Note:** For production, replace in-memory storage with Redis or a database.

### Custom Polling Intervals
Adjust polling frequency based on expected execution time:
```python
# Fast execution (check every 2 seconds)
result = client.wait_for_completion(kickoff_id, poll_interval=2)

# Slow execution (check every 30 seconds)
result = client.wait_for_completion(kickoff_id, poll_interval=30)
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CREW_URL` | Your deployed crew URL | `https://your-crew.crewai.com` |
| `CREW_TOKEN` | Authentication token | `sk_crew_...` |

## Notes

- Executions are asynchronous and may take time to complete
- Use polling or webhooks for long-running crews
- Check CrewAI AMP dashboard for detailed execution traces
- Status field names may vary (`status`, `state`, etc.)
