# Seedream API Reference

## Endpoint

```
POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations
```

## Authentication

```
Authorization: Bearer $ARK_API_KEY
Content-Type: application/json
```

Get API key: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey

## Models

| Shortname | Model ID | Capabilities |
|-----------|----------|-------------|
| seedream-5-0-lite | seedream-5-0-260128 | t2i, i2i, multi-image blend, batch, streaming, output_format |
| seedream-4-5 | seedream-4-5-250115 | t2i, i2i, multi-image blend, batch, streaming |
| seedream-4-0 | seedream-4-0-250115 | t2i, i2i, multi-image blend, batch, streaming |
| seedream-3-0-t2i | seedream-3-0-t2i-250201 | t2i only, supports seed and guidance_scale |
| seededit-3-0-i2i | seededit-3-0-i2i-250201 | i2i only (single image), supports seed and guidance_scale |

## Request Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| model | string | Model ID or endpoint ID |
| prompt | string | Text prompt (recommended <600 English words) |

### Optional

| Parameter | Type | Default | Models | Description |
|-----------|------|---------|--------|-------------|
| image | string/array | — | All except seedream-3-0-t2i | Base64 data URI or URL. Array for multi-image (2-14 images, seedream-5-0/4-5/4-0 only) |
| size | string | 2048x2048 | All | `2K`, `4K`, or `WxH` pixels. See size constraints below |
| response_format | string | url | All | `url` (24h expiry) or `b64_json` |
| watermark | boolean | true | All | Add "AI generated" watermark |
| output_format | string | jpeg | seedream-5-0-lite only | `png` or `jpeg` |
| seed | integer | -1 | seedream-3-0-t2i, seededit-3-0-i2i | Random seed [-1, 2147483647] |
| guidance_scale | float | 2.5 (t2i) / 5.5 (i2i) | seedream-3-0-t2i, seededit-3-0-i2i | Prompt adherence [1, 10] |
| sequential_image_generation | string | disabled | seedream-5-0/4-5/4-0 | `auto` (batch) or `disabled` |
| sequential_image_generation_options.max_images | integer | 15 | seedream-5-0/4-5/4-0 | Max batch images [1, 15] |
| stream | boolean | false | seedream-5-0/4-5/4-0 | Streaming output mode |
| optimize_prompt_options.mode | string | — | seedream-5-0-lite/4-5 (standard only), 4-0 | `standard` or `fast` |

### Image Input Requirements

- Formats: JPEG, PNG (seedream-5-0/4-5/4-0 also support WEBP, BMP, TIFF, GIF)
- Aspect ratio: [1/16, 16] (seedream-5-0/4-5/4-0) or [1/3, 3] (seededit-3-0)
- Width/height: >14px
- Max size: 10MB
- Max pixels: 6000x6000 = 36,000,000
- Max reference images: 14 (total input + output <= 15)

### Size Constraints by Model

**seedream-5-0-lite:** Pixels [3,686,400 — 16,777,216], ratio [1/16, 16]. Presets: `2K`, `4K`
**seedream-4-5/4-0:** Pixels [921,600 — 16,777,216], ratio [1/16, 16]. Presets: `1K`, `2K`, `4K`
**seedream-3-0-t2i:** Pixels [512x512 — 2048x2048]
**seededit-3-0-i2i:** `adaptive` only (auto-matches input aspect ratio)

### Recommended Sizes (2K)

| Ratio | WxH |
|-------|-----|
| 1:1 | 2048x2048 |
| 4:3 | 2304x1728 |
| 3:4 | 1728x2304 |
| 16:9 | 2848x1600 |
| 9:16 | 1600x2848 |
| 3:2 | 2496x1664 |
| 2:3 | 1664x2496 |
| 21:9 | 3136x1344 |

## Response

```json
{
  "model": "seedream-5-0-260128",
  "created": 1757323224,
  "data": [
    {
      "url": "https://...",
      "size": "1760x2368"
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16280,
    "total_tokens": 16280
  }
}
```

### data[] items

**Success:** `url` (when response_format=url), `b64_json` (when response_format=b64_json), `size` (WxH)
**Failure:** `error.code`, `error.message`

### Batch behavior (seedream-5-0/4-5/4-0)

- Content filter rejection: other images continue generating
- Internal error (500): remaining images are skipped

## SDK Usage

### Python (OpenAI-compatible)

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
    api_key=os.getenv('ARK_API_KEY'),
)
resp = client.images.generate(
    model="seedream-5-0-260128",
    prompt="a cat on the moon",
    size="2K",
    output_format="png",
    response_format="url",
    extra_body={"watermark": False},
)
print(resp.data[0].url)
```

### Python (BytePlus SDK)

```python
# pip install byteplus-python-sdk-v2
from byteplussdkarkruntime import Ark
client = Ark(
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
    api_key=os.getenv('ARK_API_KEY'),
)
resp = client.images.generate(
    model="seedream-5-0-260128",
    prompt="a cat on the moon",
    size="2K",
    output_format="png",
    response_format="url",
    watermark=False,
)
print(resp.data[0].url)
```

### curl

```bash
curl https://ark.ap-southeast.bytepluses.com/api/v3/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedream-5-0-260128",
    "prompt": "a cat on the moon",
    "size": "2K",
    "output_format": "png",
    "watermark": false
  }'
```
