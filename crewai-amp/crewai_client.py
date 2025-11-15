import os
import time
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class CrewAIClient:
    """Client for interacting with CrewAI AMP deployed crews."""

    def __init__(self, crew_url: str = None, crew_token: str = None):
        """
        Initialize the CrewAI client.

        Args:
            crew_url: The URL of your deployed crew (e.g., https://your-crew-url.crewai.com)
            crew_token: Bearer token for authentication
        """
        self.crew_url = crew_url or os.environ.get("CREW_URL")
        self.crew_token = crew_token or os.environ.get("CREW_TOKEN")

        if not self.crew_url:
            raise ValueError("CREW_URL must be provided or set in environment")
        if not self.crew_token:
            raise ValueError("CREW_TOKEN must be provided or set in environment")

        # Remove trailing slash from URL if present
        self.crew_url = self.crew_url.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {self.crew_token}",
            "Content-Type": "application/json"
        }

    def get_inputs(self) -> List[str]:
        """
        Retrieve the required inputs for this crew.

        Returns:
            List of required input parameter names

        Example:
            >>> client.get_inputs()
            ['topic', 'current_year']
        """
        url = f"{self.crew_url}/inputs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        return data.get("inputs", [])

    def kickoff(self, inputs: Dict[str, Any]) -> str:
        """
        Start crew execution with the provided inputs.

        Args:
            inputs: Dictionary of input parameters (e.g., {"topic": "AI", "year": "2025"})

        Returns:
            kickoff_id for tracking the execution

        Example:
            >>> kickoff_id = client.kickoff({"topic": "AI Agent Frameworks", "current_year": "2025"})
            >>> print(kickoff_id)
            'abcd1234-5678-90ef-ghij-klmnopqrstuv'
        """
        url = f"{self.crew_url}/kickoff"
        payload = {"inputs": inputs}

        response = requests.post(url, json=payload, headers=self.headers)

        # Better error handling with response details
        if not response.ok:
            try:
                error_detail = response.json()
                raise Exception(f"HTTP {response.status_code}: {error_detail}")
            except:
                response.raise_for_status()

        data = response.json()
        return data["kickoff_id"]

    def get_status(self, kickoff_id: str) -> Dict[str, Any]:
        """
        Check the execution status of a crew.

        Args:
            kickoff_id: The ID returned from kickoff()

        Returns:
            Status information as a dictionary

        Example:
            >>> status = client.get_status("abcd1234-5678-90ef-ghij-klmnopqrstuv")
            >>> print(status)
        """
        url = f"{self.crew_url}/status/{kickoff_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def wait_for_completion(
        self,
        kickoff_id: str,
        poll_interval: int = 5,
        timeout: Optional[int] = None,
        callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Poll the status endpoint until execution completes or fails.

        Args:
            kickoff_id: The ID returned from kickoff()
            poll_interval: Seconds between status checks (default: 5)
            timeout: Maximum seconds to wait (default: None = no timeout)
            callback: Optional function called with status on each poll

        Returns:
            Final status information

        Example:
            >>> def on_status(status):
            ...     print(f"Status: {status.get('state', 'unknown')}")
            >>> final = client.wait_for_completion(kickoff_id, callback=on_status)
        """
        start_time = time.time()

        while True:
            status = self.get_status(kickoff_id)

            if callback:
                callback(status)

            # Get state, handling None values
            # CrewAI AMP uses "state" field (not "status")
            state_value = status.get("state") or status.get("status") or ""
            state = state_value.upper() if isinstance(state_value, str) else ""

            # Check for completion states
            # CrewAI AMP uses uppercase states like "SUCCESS", "FAILED"
            if state in ("SUCCESS", "COMPLETED", "DONE", "FINISHED"):
                return status
            elif state in ("FAILED", "ERROR", "CANCELLED", "CANCELED"):
                raise RuntimeError(f"Execution failed with state: {state}")

            # If state is empty/None but we have a result, might be completed
            if not state and status.get("result"):
                return status

            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Execution did not complete within {timeout} seconds")

            time.sleep(poll_interval)

    def kickoff_and_wait(
        self,
        inputs: Dict[str, Any],
        poll_interval: int = 5,
        timeout: Optional[int] = None,
        callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Convenience method to kickoff and wait for completion in one call.

        Args:
            inputs: Dictionary of input parameters
            poll_interval: Seconds between status checks (default: 5)
            timeout: Maximum seconds to wait (default: None)
            callback: Optional function called with status on each poll

        Returns:
            Final status information

        Example:
            >>> result = client.kickoff_and_wait({"topic": "AI", "current_year": "2025"})
        """
        kickoff_id = self.kickoff(inputs)
        print(f"Crew execution started. Kickoff ID: {kickoff_id}")

        return self.wait_for_completion(
            kickoff_id,
            poll_interval=poll_interval,
            timeout=timeout,
            callback=callback
        )
