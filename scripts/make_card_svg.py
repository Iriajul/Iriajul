import json
from pathlib import Path

with open("data/profile.json", "r") as f:
    profile = json.load(f)

stack = ""
y = 120

for item in profile["stack"]:
    stack += f'<text x="40" y="{y}" class="text">• {item}</text>\n'
    y += 24

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="500"
     height="340"
     viewBox="0 0 500 340">

<style>

.bg {{
fill:#161b22;
}}

.title {{
fill:#58a6ff;
font-family:Consolas,monospace;
font-size:20px;
font-weight:bold;
}}

.text {{
fill:#c9d1d9;
font-family:Consolas,monospace;
font-size:16px;
}}

</style>

<rect
x="0"
y="0"
width="500"
height="340"
rx="16"
class="bg"/>

<text
x="20"
y="35"
class="title">

$ profile

</text>

<text x="40" y="70" class="text">

Name : {profile["name"]}

</text>

<text x="40" y="95" class="text">

Role : {profile["title"]}

</text>

{stack}

<text
x="40"
y="315"
class="text">

Status : {profile["status"]}

</text>

</svg>
'''

Path("assets").mkdir(exist_ok=True)

with open("assets/card.svg", "w") as f:
    f.write(svg)

print("Generated assets/card.svg")
