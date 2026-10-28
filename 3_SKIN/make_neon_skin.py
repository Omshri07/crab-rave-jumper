"""Builds jumper_neon.xml, the striped skin, from the stock robot model.

Colours and materials only: every shape, mass and joint stays as in jumper.xml.
Usage (from this folder):
    py -3.11 make_neon_skin.py ../jumper/assets/jumper/jumper.xml jumper_neon.xml
Then replay with:  play.py ... --model assets/jumper/jumper_neon.xml
(copy jumper_neon.xml into jumper/assets/jumper/ first; its meshes load by relative path).
"""
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
src = open(src_path, encoding="utf-8").read()

# name, rgba, emission
COL = {
    "V": ("neon_violet", "0.40 0.05 0.95 1", 0.2),
    "W": ("neon_white", "1.00 1.00 1.00 1", 0.5),
    "K": ("rave_black", "0.03 0.03 0.07 1", 0.0),
}
# Stripes run link by link: hip violet, thigh white, calf black, foot white.
legs = {"hip": "V", "thigh": "W", "calf": "K", "foot_tip": "W"}
arms = {"shoulder": "K", "upper_arm": "V", "forearm": "W", "palm": "K", "finger": "V",
        "finger_tip": "W", "palm_pad_f": "W", "palm_pad_b": "W",
        "finger_grip_insert": "K", "palm_grip_insert": "K"}


def pick(name):
    if name == "upper_shell_link_visual":
        return "V"
    for part, c in legs.items():
        if re.match(rf"^[LR][MR]_{part}_link_visual$", name):
            return c
    for part, c in arms.items():
        if re.match(rf"^[LR]F_{part}_link_visual$", name):
            return c
    return None


styled = 0


def repl(m):
    global styled
    c = pick(m.group(2))
    if c is None:
        return m.group(0)
    styled += 1
    mat, rgba, _ = COL[c]
    return f'{m.group(1)}{m.group(2)}{m.group(3)}rgba="{rgba}" material="{mat}"'


out = re.sub(r'(<geom name=")([^"]*_visual)("[^>]*?)rgba="[^"]*"', repl, src)
out = out.replace('rgba="0.85 0.08 0.05 1"', 'rgba="0.40 0.05 0.95 1"')  # hidden collision geoms
mats = "".join(
    f'    <material name="{n}" rgba="{r}" emission="{e}" specular="0.6" shininess="0.8"/>\n'
    for n, r, e in COL.values())
assert out.count("<asset>\n") == 1
out = out.replace("<asset>\n", "<asset>\n" + mats, 1)
open(out_path, "w", encoding="utf-8").write(out)

# Prove only colours and materials changed.
norm = lambda s: re.sub(r' material="[^"]*"', "", re.sub(r'rgba="[^"]*"', 'rgba=""', s))
assert norm(src) == norm(out.replace(mats, "")), "something other than colour changed"
print(f"{styled} visual geoms styled; only colours/materials differ from {src_path}")
