"""Hall bath (the repo's example): the room as it is in the photo (--design before), and the new
design: a Glacier Bay Highgate vanity, a Gatco oval mirror, a Kohler Cimarron toilet, Bedrosians
Cloe tile (wainscot and tub walls) and a Merola Carrara hexagon floor. The tub stays.

Built from layout.py (inches) with the shared parts in lib/roomkit. Run through ./render.sh;
options are listed in README.md. Plan coordinates: x east, y north, origin at the room's
interior NW corner.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, "lib", "roomkit")):   # the repo root
    ROOT = os.path.dirname(ROOT)
sys.path[:0] = [HERE, os.path.join(ROOT, "lib")]
import layout as L  # noqa: E402
from roomkit import core  # noqa: E402
from roomkit.core import (IN, arg, box, camera, casing_frame, cut, cylinder, dim, prism, rect_walls,  # noqa: E402
                          sky, sun, to_plan, wall_cutter, wall_run, window_portal)
from roomkit.materials import (PAINTS, basic_set, image_box_material, principled,  # noqa: E402
                               wall_tile_material)
from roomkit.parts import (alcove_tub, centerset_faucet, medicine_cabinet, oval_mirror,  # noqa: E402
                           shaker_vanity, shower_curtain, six_panel_door, towel_bar,
                           two_piece_toilet, wall_hung_sink, wall_plate)

CAMS = arg("--cams", "photo1,vanity,plan").split(",")
DESIGN = arg("--design", "new")               # before: the room as it is in the photo
NEW = DESIGN == "new"
TILE_COLOR = arg("--tile-color", "cloegreen")  # chosen: Bedrosians Cloe Green (example decision)
PAINT = arg("--paint", "warmwhite")

scene = core.start(__file__, L.CEILING)

# ---------------------------------------------------------------- materials
basic_set()
principled("bone", (0.80, 0.78, 0.72), 0.12, **{"Coat Weight": 0.5})    # old toilet: bone china
if NEW:
    principled("paint", PAINTS[PAINT], 0.65)
    # Merola Classico Carrara Hexagon 7x8: one 84" texture repeat (lib-generated, see textures/)
    image_box_material("floor", "carrara_hex.jpg", (84 * IN, 84 * IN, 84 * IN), 0.3)
    principled("base", (0.90, 0.89, 0.86), 0.3)                           # white baseboard
    principled("vanity_paint", (0.394, 0.397, 0.417), 0.45)                # Pearl Gray, from the product photo
    principled("vanity_top", (0.757, 0.730, 0.725), 0.12, **{"Coat Weight": 0.4})   # white cultured marble
    principled("curtain", (0.86, 0.85, 0.81), 0.9, **{"Sheen Weight": 0.4})
    tile, tile_pat, tile_top, tile_z0 = TILE_COLOR, "subway8", L.NEW_TILE_TOP, 4.0
    tub_tile, tub_pat = TILE_COLOR, "subway8"
else:
    principled("paint", (0.80, 0.67, 0.55), 0.6)                           # cream, from the photo
    principled("floor", (0.55, 0.51, 0.46), 0.5)                           # speckled beige sheet vinyl
    principled("base", (0.06, 0.035, 0.025), 0.4)                          # dark brown vinyl cove base
    principled("curtain", (0.02, 0.06, 0.40), 0.7)                         # royal blue shower curtain
    tile, tile_pat, tile_top, tile_z0 = "retrogreen", "square4", L.TILE_TOP, L.COVE
    tub_tile, tub_pat = "offwhite", "square4"
for ax in ("x", "y"):
    wall_tile_material(f"tile_{ax}", ax, 0.0, pattern=tile_pat, color=tile, z0=tile_z0)
    wall_tile_material(f"tile_tub_{ax}", ax, 0.0, pattern=tub_pat, color=tub_tile, z0=0.0)

# ---------------------------------------------------------------- shell
C, W, D, T, TT = L.CEILING, L.ROOM_W, L.ROOM_D, L.WALL_T, L.TILE_T
OUTLINE = [(0, 0), (W, 0), (W, -D), (0, -D)]          # interior, clockwise from the NW corner
WALLS = rect_walls(W, D)
walls = wall_run("walls", OUTLINE, T, 0, C, "paint", closed=True)
STUB_N, STUB_S = -L.TUB_L, -L.TUB_L - L.STUB_T            # the stub wall at the tub's foot
prism("stub", [(0, STUB_N), (L.TUB_W, STUB_N), (L.TUB_W, STUB_S), (0, STUB_S)], 0, C, "paint")
prism("floor", OUTLINE, -1, 0, "floor")
prism("ceiling", OUTLINE, C, C + 1, "ceiling")
base_h = 4.0 if NEW else L.COVE
base = wall_run("base", list(reversed(OUTLINE)), 0.5, 0, base_h, "base", closed=True)
box("base_stub", 0, L.TUB_W + 0.5, STUB_S - 0.5, STUB_S, 0, base_h, "base")
box("base_stub_end", L.TUB_W, L.TUB_W + 0.5, STUB_S, STUB_N, 0, base_h, "base")


def inward(frame):
    """Unit plan vector from a wall into the room."""
    r = frame[1]
    return (math.sin(r), -math.cos(r))


# ---------------------------------------------------------------- windows and door
windows = []
for k, w in enumerate(L.WINDOWS):
    f = WALLS[w["wall"]]
    x0, x1, z0, z1 = w["at"], w["at"] + w["width"], w["sill"], w["sill"] + w["height"]
    cut(walls, wall_cutter(f"cut_window_{k}", f, x0, x1, z0, z1, T))
    casing_frame(f"case_window_{k}", to_plan(f, x0), to_plan(f, x1), inward(f), z1 - z0, z0=z0, sill=True)
    mid = T / 2
    prism(f"window_glass_{k}", [to_plan(f, x0, mid - 0.1), to_plan(f, x1, mid - 0.1),
                                to_plan(f, x1, mid + 0.1), to_plan(f, x0, mid + 0.1)], z0, z1, "glass")
    box(f"window_rail_{k}", *sorted((to_plan(f, x0)[0], to_plan(f, x1)[0])), mid - 0.9, mid + 0.9,
        (z0 + z1) / 2 - 0.75, (z0 + z1) / 2 + 0.75, "trim")                 # double-hung meeting rail
    cx, cy = to_plan(f, (x0 + x1) / 2, T + 0.5)
    window_portal(f"window_portal_{k}", x1 - x0, z1 - z0, (cx, cy, (z0 + z1) / 2), (math.pi / 2, 0, f[1]))
    gx, gy = to_plan(f, (x0 + x1) / 2, mid)
    windows.append(dict(cx=gx, cy=gy, cz=(z0 + z1) / 2, w=x1 - x0, h=z1 - z0, into=list(inward(f))))

DOOR = L.DOORS[0]
f = WALLS[DOOR["wall"]]
dx0, dx1 = DOOR["at"], DOOR["at"] + DOOR["width"]
cut(walls, wall_cutter("cut_door", f, dx0, dx1, 0, DOOR["height"], T))
cut(base, wall_cutter("cut_door_base", f, dx0 - 3.6, dx1 + 3.6, -0.5, 5, T))
casing_frame("case_door", to_plan(f, dx0), to_plan(f, dx1), inward(f), DOOR["height"])
prism("threshold", [to_plan(f, dx0, 0), to_plan(f, dx1, 0), to_plan(f, dx1, T), to_plan(f, dx0, T)], -1, 0.25, "trim")
# the door stands open against the east wall, hinged on the east jamb
slab = six_panel_door("door", DOOR["width"] - 0.25, DOOR["height"] - 0.5)
hx, hy = to_plan(f, dx0, 0)
slab.location = core.I(hx - 1.6, hy + 0.2, 0.25)
slab.rotation_euler = (0, 0, math.pi / 2)
door_x0, door_x1 = sorted((to_plan(f, dx0)[0], to_plan(f, dx1)[0]))

# ---------------------------------------------------------------- wall tile
# wainscot on every wall outside the tub alcove, the tub walls tiled up to 84"
TZ0 = tile_z0
box("tile_w", 0, TT, -D, STUB_S, TZ0, tile_top, "tile_y")
box("tile_stub_s", TT, L.TUB_W, STUB_S - TT, STUB_S, TZ0, tile_top, "tile_x")
box("tile_stub_end", L.TUB_W, L.TUB_W + TT, STUB_S - TT, STUB_N, TZ0, tile_top, "tile_y")
box("tile_n", L.TUB_W, W - TT, -TT, 0, TZ0, tile_top, "tile_x")
box("tile_e", W - TT, W, -D, 0, TZ0, tile_top, "tile_y")
box("tile_s_west", TT, door_x0 - 3.6, -D, -D + TT, TZ0, tile_top, "tile_x")
box("tile_s_east", door_x1 + 3.6, W - TT, -D, -D + TT, TZ0, tile_top, "tile_x")
TUB_H, TUB_TILE = 15.0, 84.0
box("tile_tub_w", 0, TT, STUB_N, -TT, TUB_H, TUB_TILE, "tile_tub_y")
box("tile_tub_n", 0, L.TUB_W, -TT, 0, TUB_H, TUB_TILE, "tile_tub_x")
box("tile_tub_s", TT, L.TUB_W, STUB_N, STUB_N + TT, TUB_H, TUB_TILE, "tile_tub_x")

# ---------------------------------------------------------------- fixtures
alcove_tub("tub", TT, L.TUB_W, STUB_N + TT, -TT, dict(height=TUB_H))
shower_curtain("curtain", L.TUB_W - 1.0, STUB_N + TT + 0.5, STUB_N + 16, 20, 78)
cylinder("curtain_rod", 0.5, L.TUB_L, "chrome", (L.TUB_W - 1.0, STUB_N / 2, 79), rot=(math.pi / 2, 0, 0))
towel_bar("towel_bar", (L.TUB_W / 2 + TT, STUB_S - TT), 0.0, length=24, z=42)
# toilet paper holder on the east wall, beside the toilet
box("tp_post", W - TT - 2.2, W - TT, -27, -25, 25, 27, "chrome", bevel=0.3)
cylinder("tp_roll", 2.2, 4.3, "ceiling", (W - TT - 3.0, -24.0, 26), rot=(math.pi / 2, 0, 0))
if NEW:
    vy0 = -D + L.VANITY_S
    vy_c = vy0 + L.VANITY["width"] / 2
    shaker_vanity("vanity", (TT, vy0), math.pi / 2, L.VANITY)
    centerset_faucet("faucet", (TT + 2.4, vy_c), math.pi / 2, L.VANITY["height"])
    oval_mirror("mirror", (TT, vy_c), math.pi / 2, L.MIRROR)
    two_piece_toilet("toilet", L.TOILET_X, -TT, -math.pi / 2, L.NEW_TOILET)
    wall_plate("outlet_vanity", TT, vy0 + L.VANITY["width"] + 0.2 - 0.5, 42, 1, "gfci", math.pi / 2, standoff=TT)
else:
    wall_hung_sink("sink", (TT, L.OLD_SINK_Y), math.pi / 2, L.OLD_SINK)
    medicine_cabinet("cabinet", (TT, L.OLD_SINK_Y), math.pi / 2, L.OLD_CABINET)
    two_piece_toilet("toilet", L.TOILET_X, -TT, -math.pi / 2, L.OLD_TOILET)
    # plumbing access panel in the stub wall, white painted frame
    P = L.ACCESS_PANEL
    px0 = (L.TUB_W - P["width"]) / 2 + TT
    box("access_panel", px0, px0 + P["width"], STUB_S - TT - 0.6, STUB_S - TT, P["bottom"], P["bottom"] + P["height"], "trim", bevel=0.1)
    box("access_door", px0 + 1.5, px0 + P["width"] - 1.5, STUB_S - TT - 0.8, STUB_S - TT - 0.5,
        P["bottom"] + 1.5, P["bottom"] + P["height"] - 1.5, "door", bevel=0.05)

# ---------------------------------------------------------------- the hall outside the door
principled("hall_paint", (0.82, 0.80, 0.76), 0.7)
principled("hall_floor", (0.30, 0.19, 0.11), 0.4)                     # oak strip floor
HY0, HY1 = -D - T, -D - T - 42                                          # a 42" hall along the south wall
prism("hall_floor", [(-40, HY0), (W + 40, HY0), (W + 40, HY1), (-40, HY1)], -1, 0, "hall_floor")
prism("hall_ceiling", [(-40, HY0), (W + 40, HY0), (W + 40, HY1), (-40, HY1)], C, C + 1, "ceiling")
box("hall_wall_s", -44, W + 44, HY1 - 4.5, HY1, 0, C, "hall_paint")
box("hall_wall_w", -44, -40, HY1, HY0, 0, C, "hall_paint")
box("hall_wall_e", W + 40, W + 44, HY1, HY0, 0, C, "hall_paint")

# ---------------------------------------------------------------- light
# a fixture over the mirror (out of frame in the photo) plus daylight from the window
light = core.bpy.data.lights.new("vanity_light", "AREA")
light.energy = 25 * core.CAN_DIM
light.size = 18 * IN
light.color = (1.0, 0.9, 0.78)
lo = core.bpy.data.objects.new("vanity_light", light)
lo.location = core.I(8, -80, 82)
lo.rotation_euler = (0, math.radians(-25), 0)
core.link(lo)
core.LIGHTS.append(dict(name="vanity_light", x=8, y=-80, z=82, power=25))
sky()
SUN_DIR = (-0.35, -0.75, -0.55)     # bright day outside the north window
sun(SUN_DIR, energy=1.2)
principled("lawn", (0.07, 0.11, 0.04), 0.95)
box("outside_ground", -1200, 1200, -1200, 1200, -31, -30, "lawn")
box("seal_floor", -T - 50, W + T + 50, -D - T - 50, T + 50, -3, -1.2, "ceiling")
box("ceiling_seal", -T - 50, W + T + 50, -D - T - 50, T + 50, C + 1.2, C + 3, "ceiling")

# ---------------------------------------------------------------- dimension lines
dim((0, 0), (W, 0), "photo", off=-14, key="room_w")
dim((0, 0), (0, -D), "photo", off=8, key="room_d")
dim((0, -40), (L.TOILET_X, -40), "photo", off=-6, key="toilet_x")
if NEW:
    dim((0, -D), (0, -D + L.VANITY_S), "design", off=-6, key="vanity_from_south")

# ---------------------------------------------------------------- cameras
# photo1: from the doorway, matched to intake/nps-before.jpg (web/before/photo1.jpg)
camera("photo1", (32, -99, 52), (14.2, -64.1, 39), lens=12.5)   # heading 27 deg W of N, 12 down: fitted to the photo
camera("vanity", (41, -91, 62), (0, -76, 42), lens=13, level=True)
camera("plan", (W / 2, -D / 2, 400), (W / 2, -D / 2, 0), ortho=max(W, D) + 40)

# ---------------------------------------------------------------- render / export
core.finish(
    CAMS,
    info=dict(windows=windows, sun=dict(dir=list(SUN_DIR)), walk=dict(x0=L.TUB_W + 8, x1=W - 10, y0=-D + 10, y1=-34)),
    glass=("window_glass",),
)
