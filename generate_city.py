import os
import json
import urllib.request
import random
import math

def get_stats(username, token=None):
    stats = {"repos": 15, "followers": 50, "name": username.upper()}
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}")
        if token: req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            stats["repos"] = data.get("public_repos", 15)
            stats["followers"] = data.get("followers", 50)
    except: pass
    return stats

def build_city(username, stats):
    W, H = 850, 400
    random.seed(stats["repos"] + stats["followers"]) # Seed biar konsisten tapi unik
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="background:#05050A; font-family:monospace;">
    <defs><style>
        .px {{ shape-rendering: crispEdges; }}
        @keyframes blink1 {{ 0%,100%{{opacity:1}} 50%{{opacity:0.2}} }}
        @keyframes blink2 {{ 0%,100%{{opacity:0.2}} 50%{{opacity:1}} }}
        @keyframes rain {{ 0%{{transform:translateY(-20px)}} 100%{{transform:translateY({H}px)}} }}
        @keyframes fly {{ 0%{{transform:translateX(-50px)}} 100%{{transform:translateX({W+50}px)}} }}
        .n1 {{ animation: blink1 3s infinite; }} .n2 {{ animation: blink2 4s infinite; }}
        .drop {{ animation: rain 1.5s linear infinite; fill: #4A90E2; opacity: 0.4; }}
        .drone {{ animation: fly 12s linear infinite; }}
    </style></defs>
    <rect width="{W}" height="{H}" fill="#070712" class="px"/>
    """
    
    # 1. Hujan Pixel
    for i in range(80):
        x = random.randint(0, W)
        delay = random.random() * 2
        svg += f'<rect x="{x}" y="0" width="2" height="10" class="px drop" style="animation-delay:{delay:.2f}s"/>\n'

    # 2. Gedung-gedung NEWR-LABS
    num_buildings = max(8, min(25, stats["repos"] + 5))
    b_width = W // num_buildings
    neon_colors = ["#00E5FF", "#FF00E4", "#7C5CFF", "#F4D03F"]
    
    tallest_x = 0
    tallest_y = H
    
    for i in range(num_buildings):
        b_h = random.randint(120, 320)
        b_x = i * b_width
        b_y = H - b_h - 20 # Sisain ruang buat jalan
        color = random.choice(["#0B0C1A", "#121426", "#1A1A2E"])
        
        if b_y < tallest_y:
            tallest_y = b_y
            tallest_x = b_x + (b_width//2)
            
        svg += f'<rect x="{b_x}" y="{b_y}" width="{b_width-4}" height="{b_h+20}" fill="{color}" class="px"/>\n'
        
        # Jendela Neon
        for wy in range(b_y + 15, H - 30, 18):
            for wx in range(b_x + 6, b_x + b_width - 10, 12):
                if random.random() > 0.35:
                    c = random.choice(neon_colors)
                    anim = "n1" if random.random() > 0.5 else "n2"
                    svg += f'<rect x="{wx}" y="{wy}" width="6" height="10" fill="{c}" class="px {anim}"/>\n'

    # 3. Hologram NEWR-LABS di gedung tertinggi
    svg += f'<text x="{tallest_x}" y="{tallest_y - 15}" fill="#00E5FF" font-size="16" font-weight="bold" text-anchor="middle" class="px n1" style="filter: drop-shadow(0 0 5px #00E5FF);">NEWR-LABS</text>\n'

    # 4. Jalanan & Drone
    svg += f'<rect x="0" y="{H-20}" width="{W}" height="20" fill="#020205" class="px"/>\n'
    svg += """
    <g class="drone">
        <rect x="0" y="80" width="16" height="6" fill="#FF0055" class="px"/>
        <rect x="2" y="78" width="12" height="2" fill="#FFF" class="px n1"/>
        <rect x="16" y="82" width="8" height="2" fill="#00E5FF" class="px n2"/>
    </g>
    """
    
    # 5. UI Overlay
    svg += f'<text x="20" y="30" fill="#00E5FF" font-size="14" class="px">SYS.USER: {username}</text>\n'
    svg += f'<text x="20" y="50" fill="#FF00E4" font-size="12" class="px">REPOS: {stats["repos"]} | NETWORK: {stats["followers"]} NODES</text>\n'
    svg += f'<text x="{W-120}" y="30" fill="#7C5CFF" font-size="12" class="px n2">EL CAPITAN OS</text>\n'

    return svg + "</svg>"

if __name__ == "__main__":
    user = os.environ.get("GITHUB_REPOSITORY_OWNER", "drewdestar")
    token = os.environ.get("GITHUB_TOKEN")
    stats = get_stats(user, token)
    svg = build_city(user, stats)
    
    os.makedirs("dist", exist_ok=True)
    with open("dist/night_city.svg", "w") as f:
        f.write(svg)
    print("Night City generated successfully.")
