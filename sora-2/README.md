# Sora 2 Video Generation Examples

A collection of Python examples for working with the OpenAI Sora API to generate and manage AI videos.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```bash
OPENAI_API_KEY=your_api_key_here
```

## Project Files

### 01_sora_starter.py
Simple starter script with two examples:
- Long-form video (landscape 1280x720)
- Short-form video (vertical 720x1280)

Uses `create_and_poll()` for automatic waiting and downloads videos to `outputs/`.

**Run:**
```bash
python 01_sora_starter.py
```

### 02_sora_advanced.py
Interactive CLI tool with commands for managing videos.

**Commands:**
```bash
# List all videos in your library
python 02_sora_advanced.py list

# Create a new video (interactive prompts)
python 02_sora_advanced.py create

# Delete a video
python 02_sora_advanced.py delete <video_id>

# Remix a video with new prompt
python 02_sora_advanced.py remix <video_id>
```

**Features:**
- Choose between example prompts or custom videos
- Select format (long/short), model (sora-2/sora-2-pro), duration ('4', '8', '12')
- Progress bar showing generation status (updates every 2 seconds)
- Auto-download to `outputs/`

### 03_sora_fastapi.py
FastAPI server providing a REST API for video generation.

**Start server:**
```bash
python 03_sora_fastapi.py
# or
uvicorn 03_sora_fastapi:app --reload
```

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/videos` | List all videos |
| POST | `/videos/create` | Create custom video |
| POST | `/videos/create-example` | Use example prompt |
| GET | `/videos/{video_id}` | Get video status |
| DELETE | `/videos/{video_id}` | Delete video |
| POST | `/videos/{video_id}/remix` | Remix video |
| GET | `/videos/{video_id}/download` | Download video |

**Interactive docs:** http://localhost:8000/docs

**Example API calls:**

```bash
# List videos
curl http://localhost:8000/videos

# Create custom video
curl -X POST http://localhost:8000/videos/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat on a skateboard",
    "model": "sora-2",
    "seconds": "4",
    "size": "1280x720"
  }'

# Create example video
curl -X POST http://localhost:8000/videos/create-example \
  -H "Content-Type: application/json" \
  -d '{
    "example": "long_form",
    "model": "sora-2",
    "seconds": "4"
  }'

# Remix a video
curl -X POST http://localhost:8000/videos/{video_id}/remix \
  -H "Content-Type: application/json" \
  -d '{
    "remix_prompt": "Make it cyberpunk style with neon colors"
  }'

# Delete a video
curl -X DELETE http://localhost:8000/videos/{video_id}
```

## Video Parameters

### Models
- `sora-2` - Standard model
- `sora-2-pro` - Pro model

### Duration
- `'4'` - 4 seconds
- `'8'` - 8 seconds
- `'12'` - 12 seconds

### Sizes
- `1280x720` - Landscape (long-form)
- `720x1280` - Vertical (short-form/social)

## Output

All videos are saved to the `outputs/` directory with descriptive filenames.

## Video Status

- `queued` - Waiting to start
- `in_progress` - Currently generating
- `completed` - Ready to download
- `failed` - Generation failed
- `canceled` - Generation canceled

## Notes

- Progress updates poll every 2 seconds
- Videos auto-download after generation
- Remix only requires a prompt (inherits other properties from original video)
