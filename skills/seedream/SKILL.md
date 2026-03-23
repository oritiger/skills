---
name: seedream
description: "Generate and edit images using BytePlus ModelArk Seedream API. Supports text-to-image, image-to-image editing, multi-image blending, and batch generation. Use when: (1) user asks to generate/create an image from a text description, (2) edit or modify an existing image, (3) blend multiple images together, (4) create a batch/series of related images (storyboards, comics), (5) any mention of 'seedream', 'generate image', 'create picture', 'image generation', 'text to image', 'edit this image', or 'blend these images'."
---

# Seedream Image Generation

Generate and edit images via BytePlus ModelArk Seedream API.

## Prerequisites

- `ARK_API_KEY` environment variable set
- Python 3 (stdlib only, zero external dependencies)
- Get API key: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

## Quick Start

Generate an image using the bundled script:

```bash
python3 SKILL_DIR/scripts/seedream.py --prompt "a cat on the moon" --output cat.png
```

The script prints saved file paths to stdout. Always use the Read tool on the output image to show it to the user.

## Models

Default: `seedream-5-0-lite` (latest, most capable). User can specify with `--model`:

| Model | Use case |
|-------|----------|
| `seedream-5-0-lite` | Best quality. t2i, i2i, blend, batch, streaming, png output |
| `seedream-4-5` | t2i, i2i, blend, batch, streaming |
| `seedream-4-0` | t2i, i2i, blend, batch, streaming |
| `seedream-3-0-t2i` | Text-to-image only. Supports seed and guidance_scale |
| `seededit-3-0-i2i` | Single image editing only. Supports seed and guidance_scale |

## Usage Patterns

### Text-to-image

```bash
python3 SKILL_DIR/scripts/seedream.py \
  --prompt "Vibrant editorial portrait, dramatic studio lighting" \
  --size 2K --output portrait.png
```

### Image-to-image (edit existing)

```bash
python3 SKILL_DIR/scripts/seedream.py \
  --prompt "Change the background to a sunset beach" \
  --image input.jpg --output edited.png
```

Input accepts local file paths or URLs.

### Multi-image blending

```bash
python3 SKILL_DIR/scripts/seedream.py \
  --prompt "Replace clothing in image 1 with outfit from image 2" \
  --image person.jpg --image outfit.jpg --output blended.png
```

Up to 14 reference images. Only seedream-5-0-lite/4-5/4-0.

### Batch generation (storyboard/series)

```bash
python3 SKILL_DIR/scripts/seedream.py \
  --prompt "A 4-panel comic: Scene 1: ... Scene 2: ..." \
  --batch --max-images 4 --output storyboard.png
```

Outputs multiple files: `storyboard_1.png`, `storyboard_2.png`, etc.

### Aspect ratios

Use `--ratio` for common ratios or `--size` for exact pixels:

```bash
# Landscape 16:9
python3 SKILL_DIR/scripts/seedream.py --prompt "..." --ratio 16:9

# Portrait 9:16
python3 SKILL_DIR/scripts/seedream.py --prompt "..." --ratio 9:16

# Exact pixels
python3 SKILL_DIR/scripts/seedream.py --prompt "..." --size 2848x1600

# Resolution preset
python3 SKILL_DIR/scripts/seedream.py --prompt "..." --size 4K
```

Ratios: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`

## Script Options

| Flag | Description |
|------|-------------|
| `--prompt, -p` | Text prompt (required) |
| `--image, -i` | Input image path/URL (repeat for multi-image) |
| `--model, -m` | Model name (default: seedream-5-0-lite) |
| `--size, -s` | `2K`, `4K`, or `WxH` pixels |
| `--ratio, -r` | Aspect ratio shortcut |
| `--output, -o` | Output file path |
| `--output-format` | `png` or `jpeg` |
| `--batch` | Enable batch generation |
| `--max-images` | Max images for batch (1-15) |
| `--optimize-prompt` | `standard` or `fast` — AI-enhanced prompts |
| `--watermark` | Add AI watermark |
| `--seed` | Random seed (seedream-3.0/seededit-3.0 only) |
| `--guidance-scale` | Prompt adherence 1-10 (seedream-3.0/seededit-3.0 only) |
| `--base64` | Request base64 response instead of URL |
| `--stream` | Enable streaming output |
| `--json` | Print raw JSON response |
| `--dry-run` | Print request body without sending |

## Prompt Tips

- Keep prompts under 600 English words
- Be specific about style, lighting, composition, camera angle
- For batch: describe each scene explicitly (Scene 1: ..., Scene 2: ...)
- For image editing: describe what to change, not the full scene
- Use `--optimize-prompt standard` to let the model enhance your prompt

## API Reference

For full parameter details, size constraints, and SDK examples, read `references/api_reference.md`.
