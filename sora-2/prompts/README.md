# Sora Video Prompts Collection

A curated collection of 25 professional video generation prompts for OpenAI Sora.

## Categories

### Cinematic/Urban (01-05)
- `01_tokyo_street_fashion.txt` - Stylish urban scene with neon lights
- `02_suv_mountain_drive.txt` - Dynamic vehicle chase on mountain road
- `03_city_skyline_golden_hour.txt` - Sweeping aerial city view
- `04_rainy_cafe_window.txt` - Intimate cafe scene with atmospheric mood
- `05_neon_street_cyberpunk.txt` - Futuristic cityscape with rain

### Nature/Aerial (06-10)
- `06_amalfi_coast_church.txt` - Coastal drone shot of historic architecture
- `07_big_sur_waves.txt` - Dramatic ocean waves and cliffs
- `08_santorini_blue_hour.txt` - Greek island architecture at twilight
- `09_wooly_mammoths_snow.txt` - Prehistoric animals in winter landscape
- `10_forest_sunrise_mist.txt` - Atmospheric forest with morning fog

### Creative/Surreal (11-15)
- `11_pirate_ships_coffee.txt` - Miniature ships in coffee cup
- `12_cathedral_of_cats.txt` - Fantasy scene with cat kingdom
- `13_underwater_tea_party.txt` - Victorian tea party on ocean floor
- `14_floating_islands.txt` - Fantastical sky islands
- `15_paper_city.txt` - Origami city come to life

### Animals/Wildlife (16-20)
- `16_golden_retriever_surfing.txt` - Dog surfing in slow motion
- `17_hummingbird_macro.txt` - Extreme closeup of hummingbird
- `18_lion_pride_savanna.txt` - African wildlife documentary style
- `19_jellyfish_ballet.txt` - Bioluminescent underwater dance
- `20_penguin_colony_antarctica.txt` - Antarctic penguin colony

### Sci-Fi/Fantasy (21-25)
- `21_space_station_orbit.txt` - Orbital space station scene
- `22_dragon_mountain_flight.txt` - Epic dragon flying over mountains
- `23_cyberpunk_market.txt` - Future Asian night market
- `24_enchanted_forest_portal.txt` - Magical portal in ancient forest
- `25_robot_garden.txt` - Gentle robot tending rooftop garden

## Usage

Use these prompts with any of the Sora scripts:

```bash
# With CLI tool
python 02_sora_advanced.py create
# Then paste prompt when asked

# With starter script
# Copy prompt content and use in the script

# With FastAPI
curl -X POST http://localhost:8000/videos/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<paste prompt here>",
    "model": "sora-2",
    "seconds": "4",
    "size": "1280x720"
  }'
```

## Tips

- Adjust video size based on prompt content (landscape vs vertical)
- Consider duration - complex scenes may need 8-12 seconds
- Experiment with different models (sora-2 vs sora-2-pro)
- Modify prompts to match your creative vision
