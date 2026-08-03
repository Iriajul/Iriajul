"""Generate the neofetch-style info card SVG from data/profile.json.

Terminal window with traffic-light chrome, an info block, a two-column tech
stack, and a status line. Height is computed from the content so the stack can
grow without overflowing. Rows fade in with a staggered delay.
"""

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH = 520
PAD = 20          # outer padding
INSET = 15        # window inset from the outer edge
LINE = 26         # info-row line height
ROW = 26          # stack-row height

profile = json.loads(Path("data/profile.json").read_text())
stack = profile["stack"]

# Split the stack into two balanced columns (column-major so it reads down).
n_left = math.ceil(len(stack) / 2)
col_left = stack[:n_left]
col_right = stack[n_left:]
stack_rows = max(len(col_left), len(col_right))

# --- vertical layout: track a running y cursor -----------------------------
els = []
delay = 0.0


def add(markup: str, animate: bool = True) -> None:
    global delay
    if animate:
        els.append(
            f'<g class="fade" style="animation-delay:{round(delay, 2)}s">{markup}</g>'
        )
        delay += 0.12
    else:
        els.append(markup)


# Window chrome
els.append(f'<rect x="0" y="0" width="{WIDTH}" height="__H__" rx="18" class="bg"/>')
els.append(
    f'<rect x="{INSET}" y="{INSET}" width="{WIDTH - 2 * INSET}" '
    f'height="__WH__" rx="12" class="window"/>'
)
els.append('<circle cx="45" cy="45" r="7" fill="#ff5f56"/>')
els.append('<circle cx="67" cy="45" r="7" fill="#ffbd2e"/>')
els.append('<circle cx="89" cy="45" r="7" fill="#27c93f"/>')

y = 95
add(f'<text x="35" y="{y}" class="prompt">$ profile</text>')

y += 40
for label, value in (
    ("Name", profile["name"]),
    ("Role", profile["title"]),
    ("Where", profile.get("location", "")),
):
    add(
        f'<text x="35" y="{y}" class="key">{label}</text>'
        f'<text x="110" y="{y}" class="val">{escape(value)}</text>'
    )
    y += LINE

y += 12
add(f'<line x1="35" y1="{y}" x2="{WIDTH - 35}" y2="{y}" class="rule"/>', animate=False)
y += 28
add(f'<text x="35" y="{y}" class="section">tech stack</text>')

y += 30
grid_top = y
for i in range(stack_rows):
    row_y = grid_top + i * ROW
    if i < len(col_left):
        add(
            f'<rect x="35" y="{row_y - 11}" width="10" height="10" rx="2" class="dot"/>'
            f'<text x="55" y="{row_y}" class="val">{escape(col_left[i])}</text>'
        )
    if i < len(col_right):
        add(
            f'<rect x="285" y="{row_y - 11}" width="10" height="10" rx="2" class="dot"/>'
            f'<text x="305" y="{row_y}" class="val">{escape(col_right[i])}</text>'
        )
y = grid_top + stack_rows * ROW

y += 6
add(f'<line x1="35" y1="{y}" x2="{WIDTH - 35}" y2="{y}" class="rule"/>', animate=False)
y += 28
add(
    f'<text x="35" y="{y}" class="key">status</text>'
    f'<text x="110" y="{y}" class="status">{escape(profile["status"])}</text>'
)

HEIGHT = y + 24
WIN_HEIGHT = HEIGHT - 2 * INSET

body = "\n".join(els).replace("__H__", str(HEIGHT)).replace("__WH__", str(WIN_HEIGHT))

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.bg {{ fill:#0d1117; }}

.window {{
    fill:#161b22;
    stroke:#30363d;
    stroke-width:2;
}}

.rule {{ stroke:#30363d; stroke-width:1; }}

.prompt {{
    fill:#3fb950;
    font-family:Consolas,Monaco,monospace;
    font-size:20px;
    font-weight:bold;
}}

.section {{
    fill:#58a6ff;
    font-family:Consolas,Monaco,monospace;
    font-size:15px;
    font-weight:bold;
    letter-spacing:1px;
}}

.key {{
    fill:#8b949e;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.val {{
    fill:#c9d1d9;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.status {{
    fill:#3fb950;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.dot {{ fill:#3fb950; }}

.fade {{
    opacity:0;
    animation:fadeIn .6s forwards;
}}

@keyframes fadeIn {{
    from {{ opacity:0; transform:translateY(6px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}

</style>

{body}

</svg>
'''

Path("assets").mkdir(exist_ok=True)
Path("assets/card.svg").write_text(svg)

print(f"Generated assets/card.svg ({len(stack)} stack items, height {HEIGHT})")
