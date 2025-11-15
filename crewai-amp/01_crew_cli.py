import sys
import json
import argparse
from crewai_client import CrewAIClient


def cmd_inputs():
    """Command: Get required inputs for the crew."""
    client = CrewAIClient()
    inputs = client.get_inputs()

    print("\n=== Required Inputs ===\n")
    if inputs:
        for i, input_name in enumerate(inputs, 1):
            print(f"{i}. {input_name}")
    else:
        print("No required inputs")
    print()


def cmd_kickoff():
    """Command: Start crew execution."""
    client = CrewAIClient()

    print("\n=== Kickoff Crew Execution ===\n")

    # Get required inputs
    required_inputs = client.get_inputs()

    if not required_inputs:
        print("This crew requires no inputs.")
        confirm = input("Start execution? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
        inputs_dict = {}
    else:
        print(f"Required inputs: {', '.join(required_inputs)}\n")

        inputs_dict = {}
        for input_name in required_inputs:
            value = input(f"Enter value for '{input_name}': ").strip()
            inputs_dict[input_name] = value

    print(f"\nInputs to send:")
    print(json.dumps(inputs_dict, indent=2))

    confirm = input("\nProceed with kickoff? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    try:
        kickoff_id = client.kickoff(inputs_dict)
        print(f"\n✓ Crew execution started!")
        print(f"Kickoff ID: {kickoff_id}")
        print(f"\nUse 'python 01_crew_cli.py status {kickoff_id}' to check status")
    except Exception as e:
        print(f"\n✗ Failed to start execution: {e}")
        sys.exit(1)


def cmd_status(kickoff_id: str):
    """Command: Check execution status."""
    client = CrewAIClient()

    print(f"\n=== Execution Status ===\n")
    print(f"Kickoff ID: {kickoff_id}\n")

    try:
        status = client.get_status(kickoff_id)
        print(json.dumps(status, indent=2))
    except Exception as e:
        print(f"✗ Failed to get status: {e}")
        sys.exit(1)


def cmd_run():
    """Command: Kickoff and wait for completion."""
    client = CrewAIClient()

    print("\n=== Run Crew (Kickoff & Wait) ===\n")

    # Get required inputs
    required_inputs = client.get_inputs()

    if not required_inputs:
        print("This crew requires no inputs.")
        confirm = input("Start execution? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
        inputs_dict = {}
    else:
        print(f"Required inputs: {', '.join(required_inputs)}\n")

        inputs_dict = {}
        for input_name in required_inputs:
            value = input(f"Enter value for '{input_name}': ").strip()
            inputs_dict[input_name] = value

    print(f"\nInputs to send:")
    print(json.dumps(inputs_dict, indent=2))

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    def on_status_update(status):
        """Callback for status updates."""
        state = status.get("status", status.get("state", "unknown"))
        print(f"Status: {state}")

    try:
        print("\nStarting execution...\n")
        result = client.kickoff_and_wait(
            inputs_dict,
            poll_interval=5,
            callback=on_status_update
        )

        print("\n✓ Execution completed!")
        print("\nFinal result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n✗ Execution failed: {e}")
        sys.exit(1)


def cmd_wait(kickoff_id: str):
    """Command: Wait for an existing execution to complete."""
    client = CrewAIClient()

    print(f"\n=== Waiting for Execution ===\n")
    print(f"Kickoff ID: {kickoff_id}\n")

    def on_status_update(status):
        """Callback for status updates."""
        state = status.get("status", status.get("state", "unknown"))
        print(f"Status: {state}")

    try:
        result = client.wait_for_completion(
            kickoff_id,
            poll_interval=5,
            callback=on_status_update
        )

        print("\n✓ Execution completed!")
        print("\nFinal result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n✗ Execution failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CrewAI AMP CLI - Manage and execute deployed crews",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get required inputs
  python 01_crew_cli.py inputs

  # Start execution (interactive)
  python 01_crew_cli.py kickoff

  # Check status
  python 01_crew_cli.py status <kickoff_id>

  # Run and wait for completion (interactive)
  python 01_crew_cli.py run

  # Wait for existing execution
  python 01_crew_cli.py wait <kickoff_id>

Environment Variables:
  CREW_URL    - Your crew URL (e.g., https://your-crew-url.crewai.com)
  CREW_TOKEN  - Your crew authentication token
        """
    )

    parser.add_argument(
        'command',
        choices=['inputs', 'kickoff', 'status', 'run', 'wait'],
        help='Command to execute'
    )

    parser.add_argument(
        'kickoff_id',
        nargs='?',
        help='Kickoff ID (required for status and wait commands)'
    )

    args = parser.parse_args()

    # Execute command
    if args.command == 'inputs':
        cmd_inputs()
    elif args.command == 'kickoff':
        cmd_kickoff()
    elif args.command == 'status':
        if not args.kickoff_id:
            print("Error: kickoff_id is required for status command")
            print("Usage: python 01_crew_cli.py status <kickoff_id>")
            sys.exit(1)
        cmd_status(args.kickoff_id)
    elif args.command == 'run':
        cmd_run()
    elif args.command == 'wait':
        if not args.kickoff_id:
            print("Error: kickoff_id is required for wait command")
            print("Usage: python 01_crew_cli.py wait <kickoff_id>")
            sys.exit(1)
        cmd_wait(args.kickoff_id)


if __name__ == "__main__":
    main()
