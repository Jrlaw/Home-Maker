"""Mark the recessed cans on a room's top-down plan render, with each can's distance from the
west and north walls. Usage (from the room folder, after rendering --cams plan and exporting):
    python3 ../../../../lib/tools/light_plan.py renders/plan.jpg web/scene.json lights.jpg [skip_prefix ...]
skip_prefix: can names left out (e.g. can_bed for cans outside the plan view)."""
import json
import subprocess
import sys

plan, scene_json, out = sys.argv[1:4]
skip = tuple(sys.argv[4:])
info = json.load(open(scene_json))
cam = info["cameras"]["plan"]
CX, CY = cam["target"][0], cam["target"][1]          # plan camera target and ortho width (inches)
SPAN = cam["ortho"]
W = int(subprocess.check_output(["magick", "identify", "-format", "%w", plan]))


def px(x, y):
    return (x - CX) / SPAN * W + W / 2, W / 2 - (y - CY) / SPAN * W


draw, legend = [], []
for l in info["lights"]:
    if skip and l["name"].startswith(skip):
        continue
    tag = l["name"].split("_", 1)[1][:6]
    u, v = px(l["x"], l["y"])
    r = 3.4 / SPAN * W * 1.6
    draw += ["-fill", "#ffd23f", "-stroke", "#7a5200", "-strokewidth", "3",
             "-draw", f"circle {u:.0f},{v:.0f} {u + r:.0f},{v:.0f}",
             "-fill", "#2b2200", "-stroke", "none", "-pointsize", str(int(W / 45)),
             "-draw", f"text {u - W / 140:.0f},{v + W / 110:.0f} '{tag[0].upper()}'"]
    # distances from the room's west wall (x=0) and north wall (y=0)
    legend.append(f"{tag}:  {l['x']:.0f}\" from west wall,  {-l['y']:.0f}\" from north wall")

note = "\n".join(legend)
subprocess.check_call(["magick", plan, *draw,
                       "-gravity", "south", "-background", "#f2f1ec", "-splice", f"0x{int(W * 0.30)}",
                       "-fill", "#222", "-pointsize", str(int(W / 52)), "-gravity", "southwest",
                       "-annotate", f"+{int(W * 0.04)}+{int(W * 0.02)}", note,
                       "-gravity", "north", "-splice", f"0x{int(W * 0.06)}", "-pointsize", str(int(W / 36)),
                       "-annotate", "+0+12", "Recessed lights (top view, north up)", out])
print(out)
