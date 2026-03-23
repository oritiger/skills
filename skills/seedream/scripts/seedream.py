#!/usr/bin/env python3
"""Seedream image generation via BytePlus ModelArk API.

Usage:
  python3 seedream.py --prompt "a cat on the moon" [options]
  python3 seedream.py --prompt "edit the background" --image photo.jpg [options]
  python3 seedream.py --prompt "blend styles" --image img1.jpg --image img2.jpg [options]

Environment: ARK_API_KEY must be set. Zero external dependencies (stdlib only).
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3"
ENDPOINT = f"{BASE_URL}/images/generations"

DEFAULT_MODEL = "seedream-5-0-260128"
MODELS = {
    "seedream-5-0-lite": "seedream-5-0-260128",
    "seedream-4-5": "seedream-4-5-250115",
    "seedream-4-0": "seedream-4-0-250115",
    "seedream-3-0-t2i": "seedream-3-0-t2i-250201",
    "seededit-3-0-i2i": "seededit-3-0-i2i-250201",
}

RECOMMENDED_SIZES = {
    "1:1": "2048x2048",
    "4:3": "2304x1728",
    "3:4": "1728x2304",
    "16:9": "2848x1600",
    "9:16": "1600x2848",
    "3:2": "2496x1664",
    "2:3": "1664x2496",
    "21:9": "3136x1344",
}


def http_post_json(url: str, headers: dict, body: dict, timeout: int = 300) -> tuple:
    """POST JSON and return (status_code, response_body_dict)."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def http_download(url: str, output_path: str, timeout: int = 120) -> None:
    """Download a URL to a file."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        with open(output_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)


def encode_image(path: str) -> str:
    """Encode a local image file to base64 data URI."""
    p = Path(path)
    if not p.exists():
        print(f"Error: Image file not found: {path}", file=sys.stderr)
        sys.exit(1)
    ext = p.suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/{ext};base64,{b64}"


def resolve_image(img: str) -> str:
    """Return URL as-is, or encode local file to base64."""
    if img.startswith(("http://", "https://", "data:")):
        return img
    return encode_image(img)


def build_request(args) -> dict:
    """Build the API request body from parsed arguments."""
    model_id = MODELS.get(args.model, args.model)

    body = {
        "model": model_id,
        "prompt": args.prompt,
    }

    # Images
    if args.image:
        resolved = [resolve_image(img) for img in args.image]
        body["image"] = resolved[0] if len(resolved) == 1 else resolved

    # Size
    if args.size:
        body["size"] = args.size
    elif args.ratio:
        if args.ratio in RECOMMENDED_SIZES:
            body["size"] = RECOMMENDED_SIZES[args.ratio]
        else:
            print(f"Warning: Unknown ratio '{args.ratio}'. Use WxH format or one of: {list(RECOMMENDED_SIZES.keys())}", file=sys.stderr)

    # Output format
    if args.output_format:
        body["output_format"] = args.output_format

    # Response format
    body["response_format"] = "b64_json" if args.base64 else "url"

    # Watermark
    body["watermark"] = args.watermark

    # Seed (only seedream-3-0-t2i and seededit-3-0-i2i)
    if args.seed is not None and args.seed != -1:
        body["seed"] = args.seed

    # Guidance scale (only seedream-3-0-t2i and seededit-3-0-i2i)
    if args.guidance_scale is not None:
        body["guidance_scale"] = args.guidance_scale

    # Batch generation (only seedream-5-0-lite, 4-5, 4-0)
    if args.batch:
        body["sequential_image_generation"] = "auto"
        if args.max_images:
            body["sequential_image_generation_options"] = {
                "max_images": args.max_images
            }
    else:
        body["sequential_image_generation"] = "disabled"

    # Streaming
    if args.stream:
        body["stream"] = True

    # Prompt optimization
    if args.optimize_prompt:
        body["optimize_prompt_options"] = {"mode": args.optimize_prompt}

    return body


def save_image_from_b64(b64_data: str, output_path: str) -> str:
    """Decode base64 image data and save to file."""
    img_bytes = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    return output_path


def generate_output_path(base_output: str, index: int, total: int, fmt: str) -> str:
    """Generate output file path, adding index suffix for batch generation."""
    ext = fmt if fmt else "jpeg"
    if base_output:
        p = Path(base_output)
        if total > 1:
            return str(p.parent / f"{p.stem}_{index + 1}.{ext}")
        if p.suffix:
            return str(p)
        return f"{base_output}.{ext}"
    timestamp = int(time.time())
    if total > 1:
        return f"seedream_{timestamp}_{index + 1}.{ext}"
    return f"seedream_{timestamp}.{ext}"


def main():
    parser = argparse.ArgumentParser(description="Generate images with Seedream via BytePlus ModelArk")
    parser.add_argument("--prompt", "-p", required=True, help="Text prompt for image generation")
    parser.add_argument("--image", "-i", action="append", help="Input image (local path or URL). Repeat for multi-image blending.")
    parser.add_argument("--model", "-m", default="seedream-5-0-lite",
                        help=f"Model name or ID. Shortcuts: {', '.join(MODELS.keys())}. Default: seedream-5-0-lite")
    parser.add_argument("--size", "-s", help="Output size: '2K', '4K', or WxH pixels (e.g. '2048x2048')")
    parser.add_argument("--ratio", "-r", help=f"Aspect ratio shortcut: {', '.join(RECOMMENDED_SIZES.keys())}")
    parser.add_argument("--output", "-o", help="Output file path (default: seedream_<timestamp>.<fmt>)")
    parser.add_argument("--output-format", choices=["png", "jpeg"], default=None, help="Image format (default: jpeg, png for seedream-5-0-lite)")
    parser.add_argument("--base64", action="store_true", help="Request base64 response instead of URL")
    parser.add_argument("--watermark", action="store_true", default=False, help="Add AI watermark")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (seedream-3-0/seededit-3.0 only)")
    parser.add_argument("--guidance-scale", type=float, default=None, help="Prompt adherence 1-10 (seedream-3.0/seededit-3.0 only)")
    parser.add_argument("--batch", action="store_true", help="Enable batch generation (seedream-5.0/4.5/4.0)")
    parser.add_argument("--max-images", type=int, default=None, help="Max images for batch generation (1-15)")
    parser.add_argument("--stream", action="store_true", help="Enable streaming output")
    parser.add_argument("--optimize-prompt", choices=["standard", "fast"], default=None, help="Prompt optimization mode")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")
    parser.add_argument("--dry-run", action="store_true", help="Print request body without sending")

    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key and not args.dry_run:
        print("Error: ARK_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API key at: https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey", file=sys.stderr)
        sys.exit(1)

    body = build_request(args)

    if args.dry_run:
        print(json.dumps(body, indent=2))
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"Generating image with {body['model']}...", file=sys.stderr)
    status, result = http_post_json(ENDPOINT, headers, body)

    if isinstance(result, str):
        print(f"Error {status}: {result}", file=sys.stderr)
        sys.exit(1)

    if status != 200:
        print(f"Error {status}: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    # Check for top-level error
    if result.get("error"):
        print(f"API Error: {result['error'].get('code')} - {result['error'].get('message')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])
    if not data:
        print("Error: No images returned.", file=sys.stderr)
        sys.exit(1)

    fmt = args.output_format or ("png" if "5-0" in body["model"] else "jpeg")
    saved = []

    for idx, item in enumerate(data):
        # Check for per-image error
        if item.get("error"):
            err = item["error"]
            print(f"Image {idx + 1} failed: {err.get('code')} - {err.get('message')}", file=sys.stderr)
            continue

        output_path = generate_output_path(args.output, idx, len(data), fmt)

        if item.get("url"):
            http_download(item["url"], output_path)
        elif item.get("b64_json"):
            save_image_from_b64(item["b64_json"], output_path)
        else:
            print(f"Image {idx + 1}: No URL or base64 data returned.", file=sys.stderr)
            continue

        size_info = f" ({item['size']})" if item.get("size") else ""
        print(f"Saved: {output_path}{size_info}", file=sys.stderr)
        saved.append(output_path)

    usage = result.get("usage", {})
    if usage:
        print(f"Generated: {usage.get('generated_images', '?')} image(s), "
              f"Tokens: {usage.get('total_tokens', '?')}", file=sys.stderr)

    # Print paths to stdout for piping
    for p in saved:
        print(p)


if __name__ == "__main__":
    main()
