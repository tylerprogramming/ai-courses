import os
import time
import requests
from typing import Optional, Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

app = FastAPI(
    title="Sora Video API",
    description="API for managing and creating videos with OpenAI Sora",
    version="1.0.0"
)

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

# Pydantic models
class CreateVideoRequest(BaseModel):
    prompt: str
    model: Literal["sora-2", "sora-2-pro"] = "sora-2"
    seconds: Literal['4', '8', '12'] = '4'
    size: Literal["1280x720", "720x1280"] = "1280x720"

class CreateExampleRequest(BaseModel):
    example: Literal["long_form", "short_form"]
    model: Literal["sora-2", "sora-2-pro"] = "sora-2"
    seconds: Literal['4', '8', '12'] = '4'

class RemixVideoRequest(BaseModel):
    remix_prompt: str

class VideoResponse(BaseModel):
    id: str
    status: str
    model: str
    seconds: str
    size: str
    created_at: int
    progress: Optional[int] = None

# Helper functions
def create_video_with_progress(prompt: str, *, model="sora-2", seconds='4', size="1280x720", poll_interval=2):
    """Create a Sora video with polling."""
    print(f"Creating video with prompt: '{prompt}'")
    print(f"Model: {model}, Duration: {seconds}s, Size: {size}\n")

    video = openai.videos.create(
        model=model,
        prompt=prompt,
        seconds=seconds,
        size=size
    )

    print(f"Video generation started. ID: {video.id}\n")

    # Poll with progress updates
    while video.status in ("in_progress", "queued"):
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)
        print(f"Status: {video.status}, Progress: {progress}%")
        time.sleep(poll_interval)

    print(f"\nFinal status: {video.status}")

    if video.status == STATUS_FAILED:
        message = getattr(
            getattr(video, "error", None), "message", "Video generation failed"
        )
        raise RuntimeError(f"Video generation failed: {message}")

    return video

def download_video(video_id: str, output_path: str):
    """Download the generated video."""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    content = openai.videos.download_content(video_id, variant="video")
    content.write_to_file(output_path)
    print(f"Saved to {output_path}")
    return output_path

def remix_video(video_id: str, remix_prompt: str, poll_interval=2):
    """Remix an existing video using the /remix endpoint."""
    print(f"Remixing video {video_id}")
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

    # Poll for completion
    while True:
        video = openai.videos.retrieve(video_id_new)
        progress = getattr(video, "progress", 0)
        print(f"Status: {video.status}, Progress: {progress}%")

        if video.status not in ("in_progress", "queued"):
            break

        time.sleep(poll_interval)

    print(f"\nFinal status: {video.status}")

    if video.status == STATUS_FAILED:
        message = getattr(
            getattr(video, "error", None), "message", "Remix failed"
        )
        raise RuntimeError(f"Remix failed: {message}")

    return video

def video_to_response(video) -> VideoResponse:
    """Convert OpenAI video object to response model."""
    return VideoResponse(
        id=video.id,
        status=video.status,
        model=video.model,
        seconds=video.seconds,
        size=video.size,
        created_at=video.created_at,
        progress=getattr(video, "progress", None)
    )

# API Endpoints

@app.get("/")
def root():
    """API root endpoint."""
    return {
        "message": "Sora Video API",
        "endpoints": {
            "list_videos": "GET /videos",
            "create_video": "POST /videos/create",
            "create_example": "POST /videos/create-example",
            "get_video": "GET /videos/{video_id}",
            "delete_video": "DELETE /videos/{video_id}",
            "remix_video": "POST /videos/{video_id}/remix",
            "download_video": "GET /videos/{video_id}/download"
        }
    }

@app.get("/videos", response_model=list[VideoResponse])
def list_videos(limit: int = 20, order: str = "desc"):
    """List all videos in library."""
    videos = openai.videos.list(limit=limit, order=order)
    return [video_to_response(v) for v in videos.data]

@app.post("/videos/create", response_model=VideoResponse)
def create_video(request: CreateVideoRequest):
    """Create a custom video."""
    try:
        video = create_video_with_progress(
            prompt=request.prompt,
            model=request.model,
            seconds=request.seconds,
            size=request.size
        )

        # Auto-download
        output_name = f"custom_{int(time.time())}.mp4"
        download_video(video.id, f"outputs/{output_name}")

        return video_to_response(video)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/videos/create-example", response_model=VideoResponse)
def create_example_video(request: CreateExampleRequest):
    """Create a video using an example prompt."""
    if request.example not in EXAMPLES:
        raise HTTPException(status_code=400, detail=f"Example '{request.example}' not found")

    example = EXAMPLES[request.example]

    try:
        video = create_video_with_progress(
            prompt=example["prompt"],
            model=request.model,
            seconds=request.seconds,
            size=example["size"]
        )

        # Auto-download
        download_video(video.id, f"outputs/{example['name']}")

        return video_to_response(video)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/{video_id}", response_model=VideoResponse)
def get_video(video_id: str):
    """Get video status by ID."""
    try:
        video = openai.videos.retrieve(video_id)
        return video_to_response(video)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Video not found: {str(e)}")

@app.delete("/videos/{video_id}")
def delete_video_endpoint(video_id: str):
    """Delete a video by ID."""
    try:
        openai.videos.delete(video_id)
        return {"message": f"Video {video_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/videos/{video_id}/remix", response_model=VideoResponse)
def remix_video_endpoint(video_id: str, request: RemixVideoRequest):
    """Remix an existing video."""
    try:
        video = remix_video(
            video_id=video_id,
            remix_prompt=request.remix_prompt
        )

        # Auto-download
        output_name = f"remix_{int(time.time())}.mp4"
        download_video(video.id, f"outputs/{output_name}")

        return video_to_response(video)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/{video_id}/download")
def download_video_endpoint(video_id: str):
    """Download a completed video."""
    try:
        video = openai.videos.retrieve(video_id)

        if video.status != STATUS_COMPLETED:
            raise HTTPException(
                status_code=400,
                detail=f"Video not ready for download. Status: {video.status}"
            )

        output_path = f"outputs/{video_id}.mp4"
        download_video(video_id, output_path)

        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=f"{video_id}.mp4"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
