from pathlib import Path

WIDTH = 1000
HEIGHT = 220

svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.background {{
    fill:#0d1117;
}}

.title {{
    font-family: Consolas, Monaco, monospace;
    font-size:38px;
    fill:#58a6ff;
    font-weight:bold;
}}

.subtitle {{
    font-family: Consolas, Monaco, monospace;
    font-size:22px;
    fill:#c9d1d9;
}}

.prompt {{
    font-family: Consolas, Monaco, monospace;
    font-size:20px;
    fill:#3fb950;
}}

.cursor {{
    fill:#3fb950;
    animation: blink 1s infinite;
}}

@keyframes blink {{
    0% {{opacity:1;}}
    50% {{opacity:0;}}
    100% {{opacity:1;}}
}}

.fade {{
    opacity:0;
    animation: fadeIn .8s forwards;
}}

.delay1 {{
    animation-delay:.2s;
}}

.delay2 {{
    animation-delay:.8s;
}}

.delay3 {{
    animation-delay:1.4s;
}}

@keyframes fadeIn {{
    from {{
        opacity:0;
        transform:translateY(10px);
    }}

    to {{
        opacity:1;
        transform:translateY(0px);
    }}
}}

</style>

<rect class="background"
      x="0"
      y="0"
      width="1000"
      height="220"
      rx="18"/>

<text class="prompt"
      x="40"
      y="50">

$ whoami

</text>

<rect class="cursor"
      x="148"
      y="34"
      width="12"
      height="20"/>

<text class="title fade delay1"
      x="40"
      y="105">

Syed Riajul Islam

</text>

<text class="subtitle fade delay2"
      x="40"
      y="145">

Backend Developer

</text>

<text class="subtitle fade delay3"
      x="40"
      y="180">

Python • Django • FastAPI • Docker • AWS

</text>

</svg>
"""

Path("assets").mkdir(exist_ok=True)

with open("assets/header.svg", "w") as f:
    f.write(svg)

print("Generated assets/header.svg")
