import os
import sys
import time
import argparse
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Job status constants
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_CANCELED = "canceled"

# Example prompts
EXAMPLES = {
    "long_form": {
        "prompt": "A neon-lit drone shot over a rainy sci-fi street; shallow DOF; slow dolly; ambient city hiss.",
        "size": "1280x720",
        "name": "long_form_example.mp4"
    },
    "short_form": {
        "prompt": "Vertical street food closeups; handheld micro-jitters; sodium vapor lights.",
        "size": "720x1280",
        "name": "short_form_example.mp4"
    }
}

def create_video_with_progress(prompt: str, *, model="sora-2", seconds='4', size="1280x720", input_reference=None, poll_interval=2):
    """
    Create a Sora video with a progress bar showing generation status.
    If input_reference is a binary file handle, it will be treated as image->video.
    """
    print(f"Creating video with prompt: '{prompt}'")
    print(f"Model: {model}, Duration: {seconds}s, Size: {size}\n")

    # Create the video
    if input_reference is None:
        video = openai.videos.create(
            model=model,
            prompt=prompt,
            seconds=seconds,
            size=size
        )
    else:
        video = openai.videos.create(
            model=model,
            prompt=prompt,
            seconds=seconds,
            size=size,
            input_reference=input_reference
        )

    print(f"Video generation started. ID: {video.id}\n")

    # Poll with progress bar
    progress = getattr(video, "progress", 0)
    bar_length = 30

    while video.status in ("in_progress", "queued"):
        # Refresh status
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"

        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()
        time.sleep(poll_interval)

    # Move to next line after progress loop
    sys.stdout.write("\n\n")

    # Check for failure
    if video.status == STATUS_FAILED:
        message = getattr(
            getattr(video, "error", None), "message", "Video generation failed"
        )
        raise RuntimeError(f"Video generation failed: {message}")

    return video

def download_video(video_id: str, output_path: str):
    """Download the generated video using the official download_content method."""
    print(f"Downloading video content...")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    content = openai.videos.download_content(video_id, variant="video")
    content.write_to_file(output_path)
    print(f"Saved to {output_path}")

def list_videos(limit=20, after=None, order="desc"):
    """
    List all videos in your library.

    Args:
        limit: Maximum number of videos to return (default: 20)
        after: Video ID to start after (for pagination)
        order: Sort order - "asc" or "desc" (default: "desc")

    Returns:
        List of video objects
    """
    params = {"limit": limit, "order": order}
    if after:
        params["after"] = after

    videos = openai.videos.list(**params)
    return videos

def delete_video(video_id: str):
    """
    Delete a video from OpenAI's storage.

    Args:
        video_id: The ID of the video to delete

    Returns:
        Deletion confirmation response
    """
    print(f"Deleting video {video_id}...")
    response = openai.videos.delete(video_id)
    print(f"Video deleted successfully")
    return response

def print_video_library():
    """Print a formatted list of all videos in your library."""
    print("\n=== Your Video Library ===\n")
    videos = list_videos()

    if not videos.data:
        print("No videos found in your library.")
        return

    for video in videos.data:
        status_icon = "✓" if video.status == STATUS_COMPLETED else "✗" if video.status == STATUS_FAILED else "⋯"
        print(f"{status_icon} {video.id}")
        print(f"  Status: {video.status}")
        print(f"  Model: {video.model}")
        print(f"  Duration: {video.seconds}s, Size: {video.size}")
        print(f"  Created: {video.created_at}")
        if hasattr(video, 'progress'):
            print(f"  Progress: {video.progress}%")
        print()

def remix_video(video_id: str, remix_prompt: str, poll_interval=2):
    """
    Remix an existing video with a new prompt using the /remix endpoint.
    Returns the new remixed video object.
    """
    print(f"\nRemixing video {video_id}")
    print(f"Remix prompt: '{remix_prompt}'\n")

    # Use the raw API endpoint for remix
    url = f"https://api.openai.com/v1/videos/{video_id}/remix"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": remix_prompt
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    video_data = response.json()

    video_id_new = video_data["id"]
    print(f"Remix started. ID: {video_id_new}\n")

    # Poll with progress bar
    progress = 0
    bar_length = 30

    while True:
        video = openai.videos.retrieve(video_id_new)
        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"

        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()

        if video.status not in ("in_progress", "queued"):
            break

        time.sleep(poll_interval)

    sys.stdout.write("\n\n")

    if video.status == STATUS_FAILED:
        message = getattr(
            getattr(video, "error", None), "message", "Remix failed"
        )
        raise RuntimeError(f"Remix failed: {message}")

    return video

def cmd_list():
    """Command: List all videos in library."""
    print_video_library()

def cmd_delete(video_id: str):
    """Command: Delete a video by ID."""
    delete_video(video_id)

def cmd_create():
    """Command: Interactive video creation."""
    print("\n=== Create Video ===\n")

    # Ask if they want to use an example or custom
    print("1. Use long-form example")
    print("2. Use short-form example")
    print("3. Create custom video")
    choice = input("\nChoose option (1-3): ").strip()

    if choice == "1":
        example = EXAMPLES["long_form"]
        prompt = example["prompt"]
        size = example["size"]
        output_name = example["name"]
        model = "sora-2"
        seconds = '4'
        print(f"\nUsing long-form example:")
        print(f"Prompt: {prompt}")
    elif choice == "2":
        example = EXAMPLES["short_form"]
        prompt = example["prompt"]
        size = example["size"]
        output_name = example["name"]
        model = "sora-2"
        seconds = '4'
        print(f"\nUsing short-form example:")
        print(f"Prompt: {prompt}")
    elif choice == "3":
        # Custom video creation
        print("\nVideo format:")
        print("1. Long-form (landscape 1280x720)")
        print("2. Short-form (vertical 720x1280)")
        format_choice = input("Choose format (1-2): ").strip()

        size = "1280x720" if format_choice == "1" else "720x1280"

        print("\nVideo model:")
        print("1. sora-2")
        print("2. sora-2-pro")
        model_choice = input("Choose model (1-2): ").strip()
        model = "sora-2" if model_choice == "1" else "sora-2-pro"

        print("\nDuration (in seconds):")
        print("Options: '4', '8', '12'")
        seconds = input("Enter duration: ").strip()

        if seconds not in ['4', '8', '12']:
            print(f"Warning: '{seconds}' may not be supported. Valid options are '4', '8', '12'")

        prompt = input("\nEnter your video prompt: ").strip()

        format_name = "long_form" if format_choice == "1" else "short_form"
        output_name = f"{format_name}_{int(time.time())}.mp4"
    else:
        print("Invalid choice. Exiting.")
        return

    # Create the video
    video = create_video_with_progress(
        prompt=prompt,
        model=model,
        seconds=seconds,
        size=size
    )

    # Download if successful
    if video.status == STATUS_COMPLETED:
        print("Video generation completed successfully!")
        output_path = f"outputs/{output_name}"
        download_video(video.id, output_path)
        print(f"\n✓ Video ID: {video.id}")
    else:
        print(f"Video generation ended with status: {video.status}")

def cmd_remix(video_id: str):
    """Command: Remix an existing video."""
    print(f"\n=== Remix Video {video_id} ===\n")

    # Get remix details
    remix_prompt = input("Enter remix prompt: ").strip()

    # Remix the video (API only accepts prompt)
    remixed = remix_video(
        video_id=video_id,
        remix_prompt=remix_prompt
    )

    # Download if successful
    if remixed.status == STATUS_COMPLETED:
        print("Remix completed successfully!")
        output_path = f"outputs/remix_{int(time.time())}.mp4"
        download_video(remixed.id, output_path)
        print(f"\n✓ Remixed Video ID: {remixed.id}")
    else:
        print(f"Remix ended with status: {remixed.status}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sora Advanced CLI - Manage and create videos with OpenAI Sora API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python 02_sora_advanced.py list
  python 02_sora_advanced.py create
  python 02_sora_advanced.py delete video_123...
  python 02_sora_advanced.py remix video_123...
        """
    )

    parser.add_argument(
        'command',
        choices=['list', 'create', 'delete', 'remix'],
        help='Command to execute'
    )

    parser.add_argument(
        'video_id',
        nargs='?',
        help='Video ID (required for delete and remix commands)'
    )

    args = parser.parse_args()

    # Execute command
    if args.command == 'list':
        cmd_list()
    elif args.command == 'create':
        cmd_create()
    elif args.command == 'delete':
        if not args.video_id:
            print("Error: video_id is required for delete command")
            print("Usage: python 02_sora_advanced.py delete <video_id>")
            sys.exit(1)
        cmd_delete(args.video_id)
    elif args.command == 'remix':
        if not args.video_id:
            print("Error: video_id is required for remix command")
            print("Usage: python 02_sora_advanced.py remix <video_id>")
            sys.exit(1)
        cmd_remix(args.video_id)

if __name__ == "__main__":
    main()