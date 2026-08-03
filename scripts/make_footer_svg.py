"""Generate the full-width footer SVG from data/profile.json.

A terminal-styled contact bar with email / GitHub / location and a blinking
cursor. Writes assets/footer.svg.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH = 1000
HEIGHT = 120

profile = json.loads(Path("data/profile.json").read_text())

email = escape(profile.get("email", ""))
github = escape(profile.get("github", ""))
location = escape(profile.get("location", ""))

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.bg {{
    fill:#0d1117;
}}

.window {{
    fill:#161b22;
    stroke:#30363d;
    stroke-width:2;
}}

.prompt {{
    fill:#3fb950;
    font-family:Consolas,Monaco,monospace;
    font-size:18px;
}}

.text {{
    fill:#c9d1d9;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.key {{
    fill:#3fb950;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.sep {{
    fill:#8b949e;
    font-family:Consolas,Monaco,monospace;
    font-size:16px;
}}

.cursor {{
    fill:#3fb950;
    animation:blink 1s infinite;
}}

@keyframes blink {{
    0%,100% {{ opacity:1; }}
    50% {{ opacity:0; }}
}}

</style>

<rect width="{WIDTH}" height="{HEIGHT}" rx="18" class="bg"/>
<rect x="15" y="15" width="{WIDTH - 30}" height="{HEIGHT - 30}" rx="12" class="window"/>

<text x="35" y="55" class="prompt">$ contact --info</text>

<text x="35" y="85">
  <tspan class="key">email</tspan><tspan class="text">  {email}</tspan><tspan class="sep">   ·   </tspan><tspan class="key">github</tspan><tspan class="text">  {github}</tspan><tspan class="sep">   ·   </tspan><tspan class="key">loc</tspan><tspan class="text">  {location}</tspan>
</text>
<rect class="cursor" x="35" y="98" width="10" height="16"/>

</svg>
'''

Path("assets").mkdir(exist_ok=True)
Path("assets/footer.svg").write_text(svg)

print("Wrote assets/footer.svg")
