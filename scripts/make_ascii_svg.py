"""Render the prepared portrait as an animated ASCII-art SVG.

Downsamples the image to a character grid using a luminance density ramp,
then reveals the art row-by-row (typing effect) via staggered CSS delays.
Writes assets/ascii.svg.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

PREPPED = Path("photos/prepped.png")
FALLBACK = Path("photos/profile.jpg")
OUT = Path("assets/ascii.svg")

COLS = 70            # characters per row
FONT_SIZE = 9        # px
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE
# Dark -> light. A space for the darkest pixels, dense glyphs for the brightest.
RAMP = " .:-=+*#%@"


def load_image() -> Image.Image:
    src = PREPPED if PREPPED.exists() else FALLBACK
    if not src.exists():
        raise SystemExit(f"No image found (looked for {PREPPED} and {FALLBACK})")
    print(f"Loading {src}")
    return Image.open(src).convert("L")


def to_ascii_rows(img: Image.Image) -> list[str]:
    w, h = img.size
    # Characters are ~2x taller than wide, so halve the row count.
    rows = max(1, int(COLS * (h / w) * 0.5))
    small = img.resize((COLS, rows))
    pixels = np.asarray(small, dtype=np.float32)
    idx = (pixels / 255.0 * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[i] for i in row) for row in idx]


def build_svg(rows: list[str]) -> str:
    width = round(COLS * CHAR_W) + 40
    height = round(len(rows) * LINE_H) + 40

    lines = []
    for i, row in enumerate(rows):
        delay = round(i * 0.05, 2)
        y = 20 + (i + 1) * LINE_H
        lines.append(
            f'<text x="20" y="{y}" class="row" '
            f'style="animation-delay:{delay}s">{escape(row)}</text>'
        )
    body = "\n".join(lines)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}"
     height="{height}"
     viewBox="0 0 {width} {height}">

<style>

.bg {{
    fill:#0d1117;
}}

.row {{
    fill:#3fb950;
    font-family:Consolas,Monaco,monospace;
    font-size:{FONT_SIZE}px;
    white-space:pre;
    opacity:0;
    animation:reveal .01s forwards;
}}

@keyframes reveal {{
    to {{ opacity:1; }}
}}

</style>

<rect x="0" y="0" width="{width}" height="{height}" rx="12" class="bg"/>

{body}

</svg>
'''


def main() -> None:
    img = load_image()
    rows = to_ascii_rows(img)
    svg = build_svg(rows)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(svg)
    print(f"Wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
