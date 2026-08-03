"""Prepare the source portrait for ASCII conversion.

Steps: optional background removal (rembg) -> composite onto white ->
CLAHE local-contrast boost. Writes photos/prepped.png.

Background removal is optional: if rembg / onnxruntime are unavailable
(e.g. in a minimal CI image) the step is skipped and the raw photo is used.
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

SRC = Path("photos/profile.jpg")
OUT = Path("photos/prepped.png")


def remove_background(img: Image.Image):
    """Return an RGBA image with the background removed, or None on failure."""
    try:
        from rembg import remove
    except (Exception, SystemExit) as exc:  # rembg or onnxruntime missing
        print(f"  rembg unavailable ({exc}); skipping background removal")
        return None
    try:
        return remove(img)
    except (Exception, SystemExit) as exc:  # e.g. no onnxruntime backend
        print(f"  background removal failed ({exc}); using original")
        return None


def composite_on_white(img: Image.Image) -> Image.Image:
    """Flatten an RGBA image onto a white background."""
    if img.mode != "RGBA":
        return img.convert("RGB")
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.alpha_composite(white, img).convert("RGB")


def boost_contrast(img: Image.Image) -> Image.Image:
    """Apply CLAHE to the L channel for stronger local contrast."""
    arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(arr)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)
    merged = cv2.merge((l, a, b))
    return Image.fromarray(cv2.cvtColor(merged, cv2.COLOR_LAB2RGB))


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source photo not found: {SRC}")

    print(f"Loading {SRC}")
    img = Image.open(SRC).convert("RGBA")

    cut = remove_background(img)
    if cut is not None:
        img = cut

    img = composite_on_white(img)
    img = boost_contrast(img)

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
