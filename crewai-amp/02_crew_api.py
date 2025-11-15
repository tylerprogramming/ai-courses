from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from crewai_client import CrewAIClient
import asyncio
from datetime import datetime

app = FastAPI(
    title="CrewAI AMP Wrapper API",
    description="REST API wrapper for CrewAI AMP deployed crews",
    version="1.0.0"
)

# In-memory store for execution tracking (use Redis/DB for production)
executions = {}


class KickoffRequest(BaseModel):
    inputs: Dict[str, Any]
    wait: bool = False


class ExecutionStatus(BaseModel):
    kickoff_id: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def track_execution(kickoff_id: str, client: CrewAIClient):
    """Background task to track execution and store result."""
    try:
        result = client.wait_for_completion(kickoff_id, poll_interval=5)
        executions[kickoff_id] = {
            "kickoff_id": kickoff_id,
            "status": "completed",
            "started_at": executions[kickoff_id]["started_at"],
            "completed_at": datetime.utcnow().isoformat(),
            "result": result,
            "error": None
        }
    except Exception as e:
        executions[kickoff_id] = {
            "kickoff_id": kickoff_id,
            "status": "failed",
            "started_at": executions[kickoff_id]["started_at"],
            "completed_at": datetime.utcnow().isoformat(),
            "result": None,
            "error": str(e)
        }


@app.get("/")
def root():
    """API root endpoint."""
    return {
        "message": "CrewAI AMP Wrapper API",
        "endpoints": {
            "get_inputs": "GET /inputs",
            "kickoff": "POST /kickoff",
            "get_status": "GET /status/{kickoff_id}",
            "list_executions": "GET /executions"
        }
    }


@app.get("/inputs")
def get_inputs():
    """Get required inputs for the crew."""
    try:
        client = CrewAIClient()
        inputs = client.get_inputs()
        return {"inputs": inputs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/kickoff")
def kickoff(request: KickoffRequest, background_tasks: BackgroundTasks):
    """
    Start crew execution.

    Args:
        request: KickoffRequest with inputs and optional wait flag
        - If wait=false: Returns kickoff_id immediately
        - If wait=true: Waits for completion and returns full result
    """
    try:
        client = CrewAIClient()
        kickoff_id = client.kickoff(request.inputs)

        # Store execution info
        executions[kickoff_id] = {
            "kickoff_id": kickoff_id,
            "status": "running",
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "result": None,
            "error": None
        }

        if request.wait:
            # Wait for completion synchronously
            try:
                result = client.wait_for_completion(kickoff_id, poll_interval=5)
                executions[kickoff_id].update({
                    "status": "completed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": result
                })
                return executions[kickoff_id]
            except Exception as e:
                executions[kickoff_id].update({
                    "status": "failed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "error": str(e)
                })
                raise HTTPException(status_code=500, detail=str(e))
        else:
            # Track in background
            background_tasks.add_task(track_execution, kickoff_id, client)
            return {"kickoff_id": kickoff_id, "status": "started"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{kickoff_id}")
def get_status(kickoff_id: str):
    """
    Get execution status.

    Returns local cached status if available, otherwise queries CrewAI directly.
    """
    # Check local cache first
    if kickoff_id in executions:
        return executions[kickoff_id]

    # Query CrewAI directly
    try:
        client = CrewAIClient()
        status = client.get_status(kickoff_id)
        return {
            "kickoff_id": kickoff_id,
            "status": "unknown",
            "crew_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Execution not found: {str(e)}")


@app.get("/executions")
def list_executions():
    """List all tracked executions."""
    return {
        "executions": list(executions.values()),
        "count": len(executions)
    }


@app.delete("/executions/{kickoff_id}")
def delete_execution(kickoff_id: str):
    """Delete execution from local tracking (does not cancel on CrewAI)."""
    if kickoff_id not in executions:
        raise HTTPException(status_code=404, detail="Execution not found")

    del executions[kickoff_id]
    return {"message": f"Execution {kickoff_id} deleted from tracking"}


@app.delete("/executions")
def clear_executions():
    """Clear all tracked executions."""
    count = len(executions)
    executions.clear()
    return {"message": f"Cleared {count} executions"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
