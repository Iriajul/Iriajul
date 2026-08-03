"""Render data/contributions.json as an animated contribution heatmap SVG.

Lays out a 53-week x 7-day calendar with GitHub's green level palette and a
diagonal reveal animation (cells fade in based on week + weekday). Writes
assets/heatmap.svg.
"""

import json
from datetime import date
from pathlib import Path

SRC = Path("data/contributions.json")
OUT = Path("assets/heatmap.svg")

CELL = 13          # cell size + gap
SIZE = 11          # cell square size
PAD_X = 30
PAD_Y = 30
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"{SRC} not found; run fetch_contributions.py first")

    data = json.loads(SRC.read_text())
    days = data["days"]
    if not days:
        raise SystemExit("No days in contributions data")

    first = date.fromisoformat(days[0]["date"])
    # Column 0 starts on the Sunday of the first day's week.
    start_offset = (first.weekday() + 1) % 7  # Python Mon=0 -> GitHub Sun=0

    cells = []
    month_labels = []
    seen_months = set()
    max_col = 0

    for i, day in enumerate(days):
        pos = start_offset + i
        col = pos // 7
        row = pos % 7
        max_col = max(max_col, col)

        x = PAD_X + col * CELL
        y = PAD_Y + row * CELL
        color = COLORS[min(day["level"], 4)]
        delay = round((col + row) * 0.03, 2)

        cells.append(
            f'<rect x="{x}" y="{y}" width="{SIZE}" height="{SIZE}" rx="2" '
            f'fill="{color}" class="cell" style="animation-delay:{delay}s"/>'
        )

        d = date.fromisoformat(day["date"])
        if d.day <= 7 and d.month not in seen_months:
            seen_months.add(d.month)
            month_labels.append(
                f'<text x="{x}" y="{PAD_Y - 8}" class="label">{MONTHS[d.month - 1]}</text>'
            )

    weekday_labels = []
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = PAD_Y + row * CELL + SIZE - 1
        weekday_labels.append(
            f'<text x="{PAD_X - 8}" y="{y}" class="label" text-anchor="end">{name}</text>'
        )

    width = PAD_X + (max_col + 1) * CELL + PAD_X
    height = PAD_Y + 7 * CELL + 20

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}"
     height="{height}"
     viewBox="0 0 {width} {height}">

<style>

.bg {{
    fill:#0d1117;
}}

.label {{
    fill:#8b949e;
    font-family:Consolas,Monaco,monospace;
    font-size:10px;
}}

.cell {{
    opacity:0;
    animation:pop .4s ease forwards;
}}

@keyframes pop {{
    from {{ opacity:0; transform:scale(.4); }}
    to   {{ opacity:1; transform:scale(1); }}
}}

</style>

<rect x="0" y="0" width="{width}" height="{height}" rx="12" class="bg"/>

{chr(10).join(month_labels)}

{chr(10).join(weekday_labels)}

{chr(10).join(cells)}

</svg>
'''

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(svg)
    print(f"Wrote {OUT} ({len(cells)} cells, {max_col + 1} weeks)")


if __name__ == "__main__":
    main()
