"""Generates the Crab Rave scene spec for jumper-design (mjscene spec v1).

Run: py -3.11 make_crab_rave.py <output.scene.json>
Sizes are half-sizes, units are meters, Z is up (see jumper-design/ai/PROMPT.md).
"""
import json
import sys

NEON = ["neon_pink", "neon_cyan", "neon_lime", "neon_purple"]
TILES = 7          # 7 x 7 dance floor
PITCH = 0.40       # tile centre spacing
HALF_XY = 0.195    # leaves a 1 cm seam between tiles
HALF_Z = 0.005     # floor top is at z = 0.01
FLOOR_TOP = 2 * HALF_Z

materials = [
    {"name": "club_floor", "base": "concrete", "rgba": [0.03, 0.02, 0.07, 1]},
    {"name": "neon_pink", "base": "plastic_red", "rgba": [1.0, 0.08, 0.65, 1], "emission": 0.9},
    {"name": "neon_cyan", "base": "plastic_blue", "rgba": [0.05, 0.9, 1.0, 1], "emission": 0.9},
    {"name": "neon_lime", "base": "plastic_green", "rgba": [0.55, 1.0, 0.1, 1], "emission": 0.9},
    {"name": "neon_purple", "base": "plastic_blue", "rgba": [0.55, 0.1, 1.0, 1], "emission": 0.9},
    {"name": "speaker_black", "base": "plastic_white", "rgba": [0.05, 0.05, 0.06, 1]},
    {"name": "woofer", "base": "rubber", "rgba": [0.12, 0.12, 0.14, 1]},
    {"name": "gold_trim", "base": "metal", "rgba": [1.0, 0.78, 0.2, 1], "metallic": 1.0, "roughness": 0.25},
    {"name": "mirror", "base": "metal", "rgba": [0.85, 0.92, 1.0, 1], "reflectance": 0.7,
     "metallic": 1.0, "roughness": 0.05},
    {"name": "beach_ball", "base": "plastic_yellow", "rgba": [1.0, 0.85, 0.1, 1]},
]

objects = []

# Dance floor: a checker of neon tiles, solid so the robot stands on them.
offset = (TILES - 1) / 2
for i in range(TILES):
    for j in range(TILES):
        objects.append({
            "name": f"tile_{i}_{j}", "shape": "box", "kind": "static",
            "size": [HALF_XY, HALF_XY, HALF_Z],
            "pos": [(i - offset) * PITCH, (j - offset) * PITCH, HALF_Z],
            "material": NEON[(i + 2 * j) % len(NEON)], "friction": "concrete",
        })

# Speaker stacks at the four corners, angled at the floor. Woofers are visual only.
corners = [(2.0, 2.0, 225), (2.0, -2.0, 135), (-2.0, 2.0, 315), (-2.0, -2.0, 45)]
for n, (x, y, yaw) in enumerate(corners):
    objects.append({
        "name": f"speaker_{n}", "shape": "box", "kind": "static",
        "size": [0.2, 0.2, 0.45], "pos": [x, y, 0.45], "euler": [0, 0, yaw],
        "material": "speaker_black", "friction": "plastic",
    })
    objects.append({
        "name": f"speaker_{n}_trim", "shape": "box", "kind": "static", "collision": False,
        "size": [0.205, 0.205, 0.015], "pos": [x, y, 0.91], "euler": [0, 0, yaw],
        "material": "gold_trim",
    })
    for k, z in enumerate((0.27, 0.65)):
        objects.append({
            "name": f"speaker_{n}_woofer_{k}", "shape": "cylinder", "kind": "static",
            "collision": False, "size": [0.13, 0.02],
            "pos": [x, y, z], "euler": [90, 0, yaw + 90],
            "material": "woofer",
        })

# DJ booth along the back wall with a glowing front strip.
objects += [
    {"name": "dj_booth", "shape": "box", "kind": "static", "size": [0.3, 0.9, 0.28],
     "pos": [2.35, 0.0, 0.28], "material": "speaker_black", "friction": "plastic"},
    {"name": "dj_booth_glow", "shape": "box", "kind": "static", "collision": False,
     "size": [0.01, 0.88, 0.04], "pos": [2.04, 0.0, 0.2], "material": "neon_cyan"},
    {"name": "dj_decks", "shape": "box", "kind": "static", "collision": False,
     "size": [0.18, 0.6, 0.02], "pos": [2.3, 0.0, 0.58], "material": "gold_trim"},
]

# Light truss over the floor and a mirror ball hanging from it (visual only).
objects += [
    {"name": "truss_post_a", "shape": "cylinder", "kind": "static", "size": [0.03, 0.9],
     "pos": [-0.2, -1.9, 0.9], "material": "gold_trim"},
    {"name": "truss_post_b", "shape": "cylinder", "kind": "static", "size": [0.03, 0.9],
     "pos": [-0.2, 1.9, 0.9], "material": "gold_trim"},
    {"name": "truss_bar", "shape": "cylinder", "kind": "static", "collision": False,
     "size": [0.03, 1.9], "pos": [-0.2, 0.0, 1.8], "euler": [90, 0, 0], "material": "gold_trim"},
    {"name": "mirror_ball", "shape": "sphere", "kind": "static", "collision": False,
     "size": [0.2], "pos": [0.0, 0.0, 1.45], "material": "mirror"},
    {"name": "mirror_ball_cable", "shape": "cylinder", "kind": "static", "collision": False,
     "size": [0.005, 0.18], "pos": [0.0, 0.0, 1.65], "material": "gold_trim"},
]

# Bouncy beach balls to kick around (dynamic). Rolling friction needs condim 6.
for n, (x, y) in enumerate([(1.2, 0.9), (-1.1, -1.2), (0.6, -1.4)]):
    objects.append({
        "name": f"beach_ball_{n}", "shape": "sphere", "kind": "dynamic", "size": [0.09],
        "pos": [x, y, FLOOR_TOP + 0.09 + 0.02], "mass": 0.05, "material": "beach_ball",
        "friction": [0.6, 0.01, 0.002], "condim": 6, "contact": "bouncy",
    })

spec = {
    "name": "crab_rave",
    "title": "Crab Rave",
    "description": "A neon disco-floor arena with speaker stacks, a DJ booth, a mirror ball and beach balls.",
    "tags": ["indoor", "legged", "dance", "party"],
    "spawn": {"position": [0.0, 0.0, FLOOR_TOP], "yaw": 180, "clearance": 0.6},
    "physics": {"timestep": 0.002, "cone": "elliptic", "iterations": 150},
    "sky": {"preset": "night", "fog": False},
    "lighting": {
        "preset": "night_moon", "ambient": [0.12, 0.1, 0.2], "shadow_quality": "medium",
        "extra_lights": [
            {"name": "spot_pink", "type": "spot", "pos": [-1.2, -1.8, 2.6], "target": [0, 0, 0],
             "cutoff": 32, "exponent": 8, "diffuse": [1.0, 0.1, 0.7], "castshadow": True},
            {"name": "spot_cyan", "type": "spot", "pos": [-1.2, 1.8, 2.6], "target": [0, 0, 0],
             "cutoff": 32, "exponent": 8, "diffuse": [0.1, 0.9, 1.0], "castshadow": False},
            {"name": "spot_lime", "type": "spot", "pos": [1.8, 0.0, 2.6], "target": [0, 0, 0],
             "cutoff": 32, "exponent": 8, "diffuse": [0.6, 1.0, 0.1], "castshadow": False},
        ],
    },
    "ground": {"type": "plane", "size": [6, 6], "material": "club_floor",
               "friction": "concrete", "condim": 3},
    "defaults": {"condim": 3, "friction": "concrete", "contact": "default"},
    "materials": materials,
    "objects": objects,
    "cameras": [
        {"name": "stage_cam", "pos": [3.0, -3.0, 1.5], "target": [0.0, 0.0, 0.25], "fovy": 45},
        {"name": "front_cam", "pos": [-2.4, 0.0, 0.6], "target": [0.0, 0.0, 0.25], "fovy": 45},
        {"name": "top_cam", "pos": [0.0, 0.0, 4.5], "target": [0.0, 0.0, 0.0], "fovy": 50},
    ],
    "viewer": {"camera_pos": [3.0, -3.0, 1.5], "camera_target": [0.0, 0.0, 0.25]},
}

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)
print(f"wrote {sys.argv[1]}: {len(objects)} objects")
