"""Classify an image as OK or DEFECT using a simple red-pixel rule."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, UnidentifiedImageError


# Bright red markings are treated as a defect. Requiring red to dominate both
# other channels prevents the brown roof and door from triggering the rule.
MIN_RED = 170
MIN_CHANNEL_GAP = 65
DEFECT_PIXEL_RATIO = 0.002


def red_pixel_ratio(image_path: Path) -> float:
    """Return the fraction of pixels that look like bright red markings."""
    with Image.open(image_path) as image:
        rgb_image = image.convert("RGB")
        pixels = rgb_image.getdata()
        red_pixels = sum(
            red >= MIN_RED
            and red - green >= MIN_CHANNEL_GAP
            and red - blue >= MIN_CHANNEL_GAP
            for red, green, blue in pixels
        )
        return red_pixels / (rgb_image.width * rgb_image.height)


def classify(image_path: Path) -> str:
    """Return DEFECT when the image contains enough bright red pixels."""
    return "DEFECT" if red_pixel_ratio(image_path) >= DEFECT_PIXEL_RATIO else "OK"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print OK or DEFECT based on the amount of bright red in an image."
    )
    parser.add_argument("image", type=Path, help="path to a JPG or PNG image")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.image.is_file():
        print(f"Error: file not found: {args.image}")
        return 2

    try:
        print(classify(args.image))
    except (OSError, UnidentifiedImageError) as error:
        print(f"Error: cannot read image: {error}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
