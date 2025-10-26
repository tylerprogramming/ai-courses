import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def download_video(video_id: str, output_path: str):
    """Download the generated video."""
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Downloading video {video_id}...")
    content = openai.videos.download_content(video_id, variant="video")
    content.write_to_file(output_path)
    print(f"Saved to {output_path}")

# Example 1: Long-form video (landscape) - auto-polls until complete
print("Creating long-form video (landscape)...")
long_video = openai.videos.create_and_poll(
    model="sora-2",
    prompt="A neon-lit drone shot over a rainy sci-fi street; shallow DOF; slow dolly; ambient city hiss.",
    seconds='4',
    size="1280x720"
)

print(f"Long-form video completed. ID: {long_video.id}")
download_video(long_video.id, "outputs/long_form.mp4")

# Example 2: Short-form video (vertical/portrait) - auto-polls until complete
print("\nCreating short-form video (vertical)...")
short_video = openai.videos.create_and_poll(
    model="sora-2",
    prompt="Vertical street food closeups; handheld micro-jitters; sodium vapor lights.",
    seconds='4',
    size="720x1280"
)

print(f"Short-form video completed. ID: {short_video.id}")
download_video(short_video.id, "outputs/short_form.mp4")

print("\n✓ Both videos generated and downloaded successfully!")
