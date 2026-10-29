"""Reusable building parts and fixtures: doors, wall plates, recessed cans, wainscot, shelves,
towel hardware, plants, and the specific products modeled so far (Afhocomp vanity, Wyndham
Rebecca tub, TOTO Aquia IV toilet, Thuma Pillar Stool).

Fixtures that sit on a wall use one local frame: wall at y=0, room toward -y, x along the
wall; rot_z turns that frame onto the wall (0: north wall, pi: south wall, pi/2: west wall,
-pi/2: east wall). Inches throughout.
"""
import math
import random

import bmesh
import bpy
from mathutils import Vector

from . import core
from .core import I, IN, box, cut, cylinder, empty, link, mesh_obj, prism
from .materials import bark_material, leaf_material, principled, rug_material


def _mat(name, *args, **kw):
    """Create a material the first time a part needs it."""
    if name not in core.MATS:
        principled(name, *args, **kw)


# ---------------------------------------------------------------- doors and trim
def six_panel_door(name, width, height, mat="door", handle_side=1):
    """A 6-panel door slab in local space: x along width, y = thickness (outward +y), z up.
    Satin nickel lever both sides."""
    root = bpy.data.objects.new(name, None)
    link(root)
    t = 1.375
    box(f"{name}_slab", 0, width, -t / 2, t / 2, 0, height, mat, root, bevel=0.06)
    stile, rail = 4.5, 4.5
    pw = (width - 3 * stile) / 2
    rows = [(height - rail - 14, height - rail), (36 + rail, height - 2 * rail - 14), (rail, 36)]
    for face in (1, -1):
        for zr in rows:
            for col in range(2):
                x0 = stile + col * (pw + stile)
                y0, y1 = (t / 2, t / 2 + 0.12) if face > 0 else (-t / 2 - 0.12, -t / 2)
                box(f"{name}_panel", x0, x0 + pw, y0, y1, zr[0], zr[1], mat, root, bevel=0.1)
    hx = width - 2.5 if handle_side > 0 else 2.5
    for face in (1, -1):
        cylinder(f"{name}_rose", 1.2, 0.4, "nickel", (hx, face * (t / 2 + 0.2), 36),
                 rot=(math.pi / 2, 0, 0), parent=root)
        box(f"{name}_lever", hx - 4.5 if handle_side > 0 else hx, hx if handle_side > 0 else hx + 4.5,
            face * (t / 2 + 1.6) - 0.3, face * (t / 2 + 1.6) + 0.3, 35.6, 36.4, "nickel", root, bevel=0.15)
        box(f"{name}_neck", hx - 0.3, hx + 0.3, min(face * t / 2, face * (t / 2 + 1.6)),
            max(face * t / 2, face * (t / 2 + 1.6)), 35.7, 36.3, "nickel", root)
    return root


def wainscot_run(name, origin, rot_z, length, gaps=(), height=34):
    """Raised-panel wood wainscot with a white chair rail and dark baseboard on one wall
    (materials 'wainscot', 'wainscot_dark', 'trim'). x from 0..length; gaps: (x0, x1) left open."""
    root = empty(name, origin, rot_z)
    edges = [0.0] + [v for g in gaps for v in g] + [length]
    for a, b in zip(edges[::2], edges[1::2]):
        if b - a < 1:
            continue
        box(f"{name}_slab", a, b, -0.75, 0, 0, height, "wainscot", root)
        box(f"{name}_base", a, b, -1.1, 0, 0, 5, "wainscot_dark", root, bevel=0.1)
        box(f"{name}_rail", a, b, -1.6, 0, height, height + 2, "trim", root, bevel=0.2)
        n = max(1, round((b - a) / 26))            # ~2' panels between 3" stiles
        pw = (b - a - 3 * (n + 1)) / n
        for k in range(n):
            p0 = a + 3 + k * (pw + 3)
            for x0, x1, z0, z1 in ((p0, p0 + pw, 8, 9), (p0, p0 + pw, height - 4, height - 3),
                                   (p0, p0 + 1, 8, height - 3), (p0 + pw - 1, p0 + pw, 8, height - 3)):
                box(f"{name}_mold", x0, x1, -1.2, -0.75, z0, z1, "wainscot", root, bevel=0.15)
    return root


# ---------------------------------------------------------------- electrical and lights
def wall_plate(name, x, y, z, gangs, kind, rot_z, standoff=0.0):
    """White decora plate on a wall face at (x, y), center height z. kind: 'switch' or 'gfci'.
    standoff: thickness of tile on the wall there, so the plate sits on the tile face."""
    _mat("plate", (0.93, 0.92, 0.89), 0.35)
    root = bpy.data.objects.new(name, None)
    link(root)
    off = standoff
    root.location = I(x + off * math.sin(rot_z), y - off * math.cos(rot_z), 0)   # out toward the room
    root.rotation_euler = (0, 0, rot_z)
    w, h = 4.56 + 1.81 * (gangs - 1), 4.5
    box(f"{name}_plate", -w / 2, w / 2, -0.25, 0, z - h / 2, z + h / 2, "plate", root, bevel=0.08)
    for g in range(gangs):
        gx = -1.81 * (gangs - 1) / 2 + 1.81 * g
        if kind == "switch":      # decora rocker
            box(f"{name}_rocker", gx - 0.66, gx + 0.66, -0.45, -0.25, z - 1.3, z + 1.3, "plate", root, bevel=0.05)
            continue
        for dz in (-1.15, 1.15):  # GFCI: two receptacle faces, test/reset between
            box(f"{name}_face", gx - 0.66, gx + 0.66, -0.37, -0.25, z + dz - 0.55, z + dz + 0.55, "plate", root, bevel=0.05)
            for sx in (-0.25, 0.25):
                box(f"{name}_slot", gx + sx - 0.04, gx + sx + 0.04, -0.39, -0.35, z + dz - 0.2, z + dz + 0.2, "fixture", root)
    return root


def register(name, x0, x1, y0, y1):
    """Floor heating register (material 'register')."""
    return box(name, x0, x1, y0, y1, 0, 0.12, "register")


def can_light(name, x, y, power=60.0):
    """Recessed can in the ceiling: trim ring, glowing lens and a warm spot light.
    Evening dims it to about a third, --hero further. Listed in scene.json for the walkthrough."""
    C = core.CEILING
    cylinder(f"{name}_trim", 3.4, 0.2, "can_trim", (x, y, C - 0.1), segs=48)
    cylinder(f"{name}_lens", 2.6, 0.1, "can_lens", (x, y, C - 0.25), segs=48)
    ld = bpy.data.lights.new(name, "SPOT")
    ld.energy = power * core.CAN_DIM
    ld.color = (1.0, 0.9, 0.8)
    ld.spot_size = math.radians(115)
    ld.spot_blend = 0.6
    ld.shadow_soft_size = 2.5 * IN
    ob = bpy.data.objects.new(name, ld)
    ob.location = I(x, y, C - 0.6)
    link(ob)
    core.LIGHTS.append(dict(name=name, x=x, y=y, z=C - 0.6, power=power))


# ---------------------------------------------------------------- rounded fixtures
def plan_prism(name, pts, z0, z1, mat, parent=None, sub=2):
    """Prism from local inch points, smoothed with subdivision (for rounded fixtures)."""
    ob = prism(name, pts, z0, z1, mat, parent)
    ob.data.polygons.foreach_set("use_smooth", [True] * len(ob.data.polygons))
    b = ob.modifiers.new("bevel", "BEVEL")
    b.width = 0.6 * IN
    b.segments = 3
    if sub:
        ob.modifiers.new("sub", "SUBSURF").levels = sub
    return ob


def egg(length, half_w, back_square=True, n_front=2.3, n_back=5.0, N=48):
    """Elongated-bowl plan: x from 0 (back) to length (front), y in +-half_w."""
    pts = []
    for j in range(N):
        th = 2 * math.pi * j / N
        c, s_ = math.cos(th), math.sin(th)
        n = n_front if c > 0 else (n_back if back_square else n_front)
        x = length / 2 + (length / 2) * math.copysign(abs(c) ** (2 / n), c)
        y = half_w * math.copysign(abs(s_) ** (2 / n), s_)
        pts.append((x, y))
    return pts


def toto_aquia_toilet(x_wall, yc, rot_z=math.pi):
    """TOTO Aquia IV one-piece, skirted, dual flush 0.9/1.28 GPF (MS646124CEMFG), with a
    WASHLET bidet seat. Retailer spec: 28.25" deep, 15.2" wide, 28.4" to the tank top;
    universal-height bowl. Back against the wall at (x_wall, yc); rot_z=pi faces west."""
    root = bpy.data.objects.new("toilet", None)
    link(root)
    root.location = I(x_wall, yc, 0)
    root.rotation_euler = (0, 0, rot_z)
    # skirted bowl, then the low one-piece tank rising from its back
    plan_prism("toilet_skirt", [(x + 1.0, y) for x, y in egg(27.25, 7.4)], 0, 16.2, "ceramic", root)
    plan_prism("toilet_tank", [(x + 0.75, y) for x, y in egg(8.75, 7.6, n_front=6, n_back=6)],
               15.0, 28.4, "ceramic", root)
    for dy, r in ((1.4, 0.75), (-1.4, 0.55)):  # dual-flush push buttons on the tank lid, 5" out
        cylinder("toilet_flush", r, 0.2, "chrome", (x_wall + 5.0 * math.cos(rot_z) - dy * math.sin(rot_z),
                                                     yc + 5.0 * math.sin(rot_z) + dy * math.cos(rot_z), 28.45), segs=24)
    # WASHLET: rear housing in front of the tank, seat and lid over the bowl
    plan_prism("washlet_housing", [(x + 9.0, y) for x, y in egg(6.5, 7.3, n_front=3, n_back=5)],
               16.2, 19.6, "ceramic", root)
    plan_prism("washlet_seat", [(x + 14.0, y) for x, y in egg(14.5, 7.1, back_square=False)],
               16.25, 17.2, "ceramic", root)
    plan_prism("washlet_lid", [(x + 14.2, y) for x, y in egg(14.2, 6.9, back_square=False)],
               17.25, 18.2, "ceramic", root)
    return root


# ---------------------------------------------------------------- furniture and products
THUMA_STOOL = dict(width=20, depth=13.5, height=17.5, cushion=1.5)   # ASSUMED from photos, not listed


def pillar_stool(name, x, y, rot_z, S=THUMA_STOOL):
    """Thuma Pillar Stool with cushion: thick slab top on two tapered slab legs running
    front to back. Local frame centered on the stool, x along the seat width."""
    _mat("linen", (0.62, 0.58, 0.52), 0.9, **{"Sheen Weight": 0.3})
    root = bpy.data.objects.new(name, None)
    link(root)
    root.location = I(x, y, 0)
    root.rotation_euler = (0, 0, rot_z)
    w, d, h, t = S["width"], S["depth"], S["height"], 1.25
    box(f"{name}_top", -w / 2, w / 2, -d / 2, d / 2, h - t, h, "wood", root, bevel=0.3)
    for sx in (-1, 1):
        x0 = sx * (w / 2 - 3.5)
        box(f"{name}_leg", x0 - 1.0, x0 + 1.0, -d / 2 + 1.2, d / 2 - 1.2, 0, h - t, "wood", root, bevel=0.3)
    box(f"{name}_cushion", -w / 2 + 0.75, w / 2 - 0.75, -d / 2 + 0.75, d / 2 - 0.75, h, h + S["cushion"],
        "linen", root, bevel=0.5)
    return root


def afhocomp_vanity(name, origin, rot_z, V, M):
    """Afhocomp 48" floating vanity (MOACBV0748ESO, Brown Oak / Roma Travertine) with a Kohler
    Honesty faucet and a backlit square mirror. V: vanity dims, M: mirror dims (see layout.py).
    Local frame: wall at y=0, front toward -y, x from 0..width."""
    root = empty(name, origin, rot_z)
    w, d, top, tt = V["width"], V["depth"], V["top_h"], V["top_t"]
    zc1 = top - tt - V["reveal"]
    zc0 = top - V["height"]
    slab = box(f"{name}_top", 0, w, -d, 0, top - tt, top, "travertine", root, bevel=0.08)
    sx0, sx1, sy0, sy1 = w / 2 - 10, w / 2 + 10, -d + 3.2, -4.0
    sink_cut = box(f"{name}_sinkcut", sx0, sx1, sy0, sy1, top - 6, top + 1, None, root)
    cut(slab, sink_cut)
    slab.modifiers.move(len(slab.modifiers) - 1, 0)      # boolean before bevel
    basin = box(f"{name}_basin", sx0 - 0.3, sx1 + 0.3, sy0 - 0.3, sy1 + 0.3, top - 6.5, top - tt,
                "ceramic", root)
    bin_cut = box(f"{name}_basincut", sx0, sx1, sy0, sy1, top - 6, top + 1, None, root)
    cut(basin, bin_cut)
    cylinder(f"{name}_drain", 0.9, 0.1, "fixture", (w / 2, (sy0 + sy1) / 2, top - 6.0), parent=root)
    # recessed back (dark shadow gap) + three fronts, the left one fluted
    carcass = box(f"{name}_carcass", 0.3, w - 0.3, -V["cab_depth"] + 0.8, 0, zc0 + 0.3, zc1, "wood", root)
    basin_room = box(f"{name}_basinroom", sx0 - 0.4, sx1 + 0.4, sy0 - 0.4, sy1 + 0.4, top - 7, top + 1, None, root)
    cut(carcass, basin_room)
    fw = (w - 0.3) / 3
    for k in range(3):
        x0 = k * fw + (0.1 if k else 0)
        x1 = (k + 1) * fw - 0.05
        box(f"{name}_front{k}", x0, x1, -V["cab_depth"], -V["cab_depth"] + 0.8, zc0, zc1, "wood", root, bevel=0.04)
    n_reeds = 22
    rw = fw / n_reeds
    for r in range(n_reeds):
        c = cylinder(f"{name}_reed", rw * 0.42, zc1 - zc0 - 0.4, "wood",
                     (rw * (r + 0.5), -V["cab_depth"] - 0.05, (zc0 + zc1) / 2), segs=12, parent=root)
        c.scale = (1, 0.5, 1)
    # faucet: Kohler Honesty single-hole K-99760-4-BL (5-15/16" tall, spout 4-1/2" high,
    # 4-3/16" reach); square-profile body and spout, side lever
    fx, fy = w / 2, -2.2
    box(f"{name}_faucet_body", fx - 0.75, fx + 0.75, fy - 0.75, fy + 0.75, top, top + 5.94, "fixture", root, bevel=0.12)
    box(f"{name}_faucet_spout", fx - 0.6, fx + 0.6, fy - 4.19 - 0.1, fy - 0.75, top + 4.5, top + 5.4, "fixture", root, bevel=0.1)
    box(f"{name}_faucet_lever", fx + 0.75, fx + 3.1, fy - 0.22, fy + 0.22, top + 4.0, top + 4.9, "fixture", root, bevel=0.08)
    # mirror: glass square standing off the wall, LED strip around the back edge
    mx0 = w / 2 - M["width"] / 2
    mx1 = mx0 + M["width"]
    mz0, mz1 = M["bottom"], M["bottom"] + M["height"]
    so = M["standoff"]
    box(f"{name}_mirror_back", mx0 + 1.5, mx1 - 1.5, -so + 0.25, -0.1, mz0 + 1.5, mz1 - 1.5, "mirror_back", root)
    box(f"{name}_mirror", mx0, mx1, -so - 0.2, -so + 0.25, mz0, mz1, "mirror", root, bevel=0.1)
    for nm, a in (("l", (mx0 + 0.6, mx0 + 1.0, mz0 + 0.6, mz1 - 0.6)),
                  ("r", (mx1 - 1.0, mx1 - 0.6, mz0 + 0.6, mz1 - 0.6)),
                  ("b", (mx0 + 0.6, mx1 - 0.6, mz0 + 0.6, mz0 + 1.0)),
                  ("t", (mx0 + 0.6, mx1 - 0.6, mz1 - 1.0, mz1 - 0.6))):
        box(f"{name}_led_{nm}", a[0], a[1], -so + 0.25, -so + 0.35, a[2], a[3], "led", root)
    return root


def rebecca_tub(cx, cy, T):
    """Wyndham Collection Rebecca freestanding tub (WCOBT101460), centered at (cx, cy), long
    axis along x. T: length, width, height (ends), mid_height (sides)."""
    a_top, b_top = T["length"] / 2, T["width"] / 2
    a_bot, b_bot = a_top - 7.5, b_top - 5.5
    wall = 1.3
    floor_z = 3.0
    N, RINGS = 96, 14

    def se(theta, a, b, n=2.6):
        c, s = math.cos(theta), math.sin(theta)
        return (a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s))

    def rim_z(theta):
        return T["mid_height"] + (T["height"] - T["mid_height"]) * abs(math.cos(theta)) ** 2.2

    def flare(t):
        return math.sin(t * math.pi / 2) ** 0.75

    bm = bmesh.new()
    rings = []
    # outer shell, bottom -> rim
    for i in range(RINGS + 1):
        t = i / RINGS
        a = a_bot + (a_top - a_bot) * flare(t)
        b = b_bot + (b_top - b_bot) * flare(t)
        ring = []
        for j in range(N):
            th = 2 * math.pi * j / N
            x, y = se(th, a, b)
            ring.append(bm.verts.new(((cx + x) * IN, (cy + y) * IN, t * rim_z(th) * IN)))
        rings.append(ring)
    # inner shell, rim -> floor
    for i in range(RINGS, -1, -1):
        t = i / RINGS
        a = a_bot - 2.5 + (a_top - wall - a_bot + 2.5) * flare(t)
        b = b_bot - 2.0 + (b_top - wall - b_bot + 2.0) * flare(t)
        ring = []
        for j in range(N):
            th = 2 * math.pi * j / N
            x, y = se(th, a, b)
            z = floor_z + t * (rim_z(th) - 0.15 - floor_z)
            ring.append(bm.verts.new(((cx + x) * IN, (cy + y) * IN, z * IN)))
        rings.append(ring)
    for r0, r1 in zip(rings, rings[1:]):
        for j in range(N):
            k = (j + 1) % N
            bm.faces.new((r0[j], r0[k], r1[k], r1[j]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    core.outward(bm)
    ob = mesh_obj("tub", bm, "acrylic", smooth=True)
    ob.modifiers.new("sub", "SUBSURF").levels = 2
    # center drain + overflow on the wall-side long side
    cylinder("tub_drain", 1.6, 0.15, "fixture", (cx, cy, floor_z + 0.08))
    box("tub_overflow", cx - 1.5, cx + 1.5, cy + b_top - wall - 0.9, cy + b_top - wall - 0.3,
        T["mid_height"] - 4.5, T["mid_height"] - 3.7, "fixture", bevel=0.15)
    return ob


def rug(name, x0, x1, y0, y1, fname, flip=False):
    """Flat bath mat with a picture (textures/fname) across the top."""
    rug_material(name, fname, flip)
    box(name, x0, x1, y0, y1, 0, 0.45, name, bevel=0.35)


# ---------------------------------------------------------------- towel hardware (Kohler Honesty)
def towel_arm(name, origin, rot_z, z=50):
    """Kohler Honesty K-26637 towel arm (matte black), from the spec drawing: 2-1/8" square
    plate, short post, flat blade 9-11/16" overall that stands 2-15/16" off the wall and
    tapers toward its open end. Opens toward +x (the viewer's right, the only way it mounts).
    With a hand towel."""
    root = empty(name, origin, rot_z)
    p = 2.125 / 2
    box(f"{name}_plate", -p, p, -0.22, 0, z - p, z + p, "fixture", root, bevel=0.05)
    box(f"{name}_post", -0.65, 0.65, -2.05, -0.22, z - 0.62, z + 0.62, "fixture", root, bevel=0.06)
    end = 9.6875 - p
    blade = [(-0.65, -2.05), (end, -2.62), (end, -2.94), (-0.65, -2.94)]
    prism(f"{name}_blade", blade, z - 0.7, z + 0.7, "fixture", root)
    # hand towel folded over the blade, from the open end
    tx0, tx1 = 1.4, 8.4
    box(f"{name}_towel_front", tx0, tx1, -3.7, -3.0, z - 15, z + 0.75, "towel", root, bevel=0.3)
    box(f"{name}_towel_back", tx0, tx1, -1.95, -1.3, z - 12.5, z + 0.75, "towel", root, bevel=0.3)
    box(f"{name}_towel_fold", tx0, tx1, -3.0, -1.95, z + 0.7, z + 1.25, "towel", root, bevel=0.25)
    return root


def robe_hook(name, origin, rot_z, z=66, towel=True):
    """Kohler Honesty robe hook K-26636-BL (square plate and post like the towel arm),
    with a bath towel hanging from it."""
    root = empty(name, origin, rot_z)
    p = 2.125 / 2
    box(f"{name}_plate", -p, p, -0.22, 0, z - p, z + p, "fixture", root, bevel=0.05)
    box(f"{name}_post", -0.55, 0.55, -2.1, -0.22, z - 0.55, z + 0.55, "fixture", root, bevel=0.06)
    box(f"{name}_tip", -0.55, 0.55, -2.1, -1.4, z + 0.55, z + 1.4, "fixture", root, bevel=0.06)
    if towel:   # bath towel hung by a corner: a wide drape either side of the hook
        box(f"{name}_towel", -5, 5, -2.7, -1.4, z - 26, z + 0.6, "towel", root, bevel=0.5)
        box(f"{name}_towel_back", -4.5, 4.5, -1.3, -0.3, z - 22, z - 1.5, "towel", root, bevel=0.4)
    return root


def towel_ladder(name, origin, rot_z, width=16, height=66, lean_deg=11, mat="wood"):
    """Leaning ladder: rails at x=0 and x=width; the foot stands out from the wall, the top
    rests on it. Two towels folded over rungs."""
    root = empty(name, origin, rot_z)
    lean = math.radians(lean_deg)
    foot = height * math.sin(lean)
    rise = height * math.cos(lean)

    def out(h):      # distance from the wall at height h
        return foot * (1 - h / rise) + 0.8

    for xx in (0, width):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        rail = mesh_obj(f"{name}_rail", bm, mat, root)
        rail.scale = (0.8 * IN, 1.4 * IN, height * IN)
        rail.location = I(xx, -out(rise / 2), rise / 2)
        rail.rotation_euler = (-lean, 0, 0)
        rail.modifiers.new("bevel", "BEVEL").width = 0.15 * IN
    for k in range(5):
        h = 14 + k * 12
        cylinder(f"{name}_rung", 0.45, width, mat, (width / 2, -out(h), h), rot=(0, math.pi / 2, 0), parent=root)
    for h, wdt, drop in ((38, 12, 14), (50, 11, 18)):
        y = -out(h)
        for side in (-1, 1):
            box(f"{name}_towel", width / 2 - wdt / 2, width / 2 + wdt / 2, y + side * 0.55 - 0.35,
                y + side * 0.55 + 0.35, h - drop + (4 if side < 0 else 0), h + 0.45, "towel", root, bevel=0.3)
    return root


def shelf_ladder(name, origin, rot_z, width=18, height=66, lean_deg=12, mat="wood", props=True, hybrid=False):
    """Leaning shelf ladder: two rails like towel_ladder, with four flat shelves running back to
    the wall, deepest at the bottom. props: a few bottles, a rolled towel and a small plant.
    hybrid: two shelves up top for products, towel rungs below with two towels over them."""
    root = empty(name, origin, rot_z)
    lean = math.radians(lean_deg)
    foot = height * math.sin(lean)
    rise = height * math.cos(lean)

    def out(h):      # distance from the wall at height h
        return foot * (1 - h / rise) + 0.8

    for xx in (0, width):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        rail = mesh_obj(f"{name}_rail", bm, mat, root)
        rail.scale = (0.9 * IN, 1.6 * IN, height * IN)
        rail.location = I(xx, -out(rise / 2), rise / 2)
        rail.rotation_euler = (-lean, 0, 0)
        rail.modifiers.new("bevel", "BEVEL").width = 0.15 * IN
    heights = (44, 56) if hybrid else (12, 26, 40, 54)
    for h in heights:
        box(f"{name}_shelf", 0.45, width - 0.45, -out(h) - 0.6, -0.2, h - 0.75, h, mat, root, bevel=0.08)
    if hybrid:
        _mat("towel", (0.92, 0.91, 0.88), 0.95)
        for h in (12, 22, 32):
            cylinder(f"{name}_rung", 0.45, width, mat, (width / 2, -out(h), h), rot=(0, math.pi / 2, 0), parent=root)
        for h, wdt, drop in ((22, 13, 12), (32, 12, 15)):
            y = -out(h)
            for side in (-1, 1):
                box(f"{name}_towel", width / 2 - wdt / 2, width / 2 + wdt / 2, y + side * 0.55 - 0.35,
                    y + side * 0.55 + 0.35, h - drop + (4 if side < 0 else 0), h + 0.45, "towel", root, bevel=0.3)
        if props:
            for k, (xx, r, hh) in enumerate(((3.5, 1.1, 6), (6.5, 1.3, 4.5), (10, 0.9, 5.5), (14, 1.2, 4))):
                cylinder(f"{name}_bottle", r, hh, "ceramic" if k % 2 else "acrylic", (xx, -out(44) / 2, 44 + hh / 2), parent=root)
            cylinder(f"{name}_pot", 1.8, 3.2, "ceramic", (width - 4, -out(56) / 2, 56 + 1.6), parent=root)
        return root
    if props:
        _mat("towel", (0.92, 0.91, 0.88), 0.95)
        cylinder(f"{name}_towel_roll", 2.6, width - 4, "towel", (width / 2, -out(12) / 2 - 0.5, 12 + 2.6),
                 rot=(0, math.pi / 2, 0), parent=root)
        for k, (xx, r, hh) in enumerate(((3.5, 1.1, 6), (6.5, 1.3, 4.5), (9.5, 0.9, 5.5), (13.5, 1.2, 4))):
            cylinder(f"{name}_bottle", r, hh, "ceramic" if k % 2 else "acrylic", (xx, -out(40) / 2, 40 + hh / 2), parent=root)
        for k, (xx, r, hh) in enumerate(((4, 1.6, 3), (9, 1.4, 3.5))):
            cylinder(f"{name}_jar", r, hh, "ceramic", (xx, -out(26) / 2, 26 + hh / 2), parent=root)
        cylinder(f"{name}_pot", 1.8, 3.2, "ceramic", (width - 4, -out(54) / 2, 54 + 1.6), parent=root)
    return root


# ---------------------------------------------------------------- shelves and planters (wood: material 'wood')
def board_shelf(name, origin, rot_z, z0, width=24, depth=7, thick=1.75):
    """Plain floating board with a rolled towel and a small potted plant.
    x from 0..width."""
    root = empty(name, origin, rot_z)
    box(f"{name}_board", 0, width, -depth, 0, z0, z0 + thick, "wood", root, bevel=0.08)
    top = z0 + thick
    tl = min(9, width * 0.45)                                # rolled towel sized to the board
    cylinder(f"{name}_towel", 1.9, tl, "towel", (1.5 + tl / 2, -depth / 2, top + 1.9), rot=(0, math.pi / 2, 0), parent=root)
    px = max(width - 4, 1.5 + tl + 2.3)                     # keep the pot clear of the towel on short boards
    cylinder(f"{name}_pot", 1.8, 3.4, "pot", (px, -depth / 2, top + 1.7), parent=root)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.6 * IN)
    pl = mesh_obj(f"{name}_plant", bm, "leaves", root, smooth=True)
    pl.location = I(px, -depth / 2, top + 5.6)
    return root


FLOATING_SHELF = dict(width=24, depth=7, height=5.25, box_w=10, t=0.75, lip=1.75)


def floating_shelf(name, origin, rot_z, z0, SH=FLOATING_SHELF, props=True):
    """Open tray on the left, closed fluted box on the right (after the Cubette example).
    SH: width, depth, height, box_w, t, lip. x from 0..width."""
    root = empty(name, origin, rot_z)
    w, d, h, bw, t = SH["width"], SH["depth"], SH["height"], SH["box_w"], SH["t"]
    tray_w = w - bw
    box(f"{name}_tray", 0, tray_w, -d, 0, z0, z0 + t, "wood", root, bevel=0.06)
    box(f"{name}_back", 0, tray_w, -t, 0, z0 + t, z0 + SH["lip"] + t, "wood", root, bevel=0.06)
    box(f"{name}_end", 0, t, -d, -t, z0 + t, z0 + SH["lip"] + t, "wood", root, bevel=0.06)
    box(f"{name}_box", tray_w, w, -d + 0.4, 0, z0, z0 + h - 0.6, "wood", root, bevel=0.04)
    box(f"{name}_lid", tray_w - 0.1, w + 0.1, -d - 0.1, 0, z0 + h - 0.6, z0 + h, "wood", root, bevel=0.08)
    n = 13
    rw = bw / n
    for r in range(n):
        c = cylinder(f"{name}_reed", rw * 0.42, h - 0.9, "wood",
                     (tray_w + rw * (r + 0.5), -d + 0.4, z0 + (h - 0.6) / 2), segs=12, parent=root)
        c.scale = (1, 0.5, 1)
    if props:   # a rolled hand towel and a small plant pot, for scale
        cylinder(f"{name}_towel", 1.9, 9, "towel", (6.5, -d / 2, z0 + t + 1.9), rot=(0, math.pi / 2, 0), parent=root)
        cylinder(f"{name}_pot", 1.8, 3.4, "pot", (tray_w - 2.6, -d / 2, z0 + t + 1.7), parent=root)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.6 * IN)
        pl = mesh_obj(f"{name}_plant", bm, "leaves", root, smooth=True)
        pl.location = I(tray_w - 2.6, -d / 2, z0 + t + 5.6)
    return root


def open_box(name, origin, rot_z, x0, z0, w=10, h=10, d=6, t=0.75, prop=None):
    """Open cube shelf (no front or back); x0/z0 is the box's lower-left corner along the wall.
    prop: 'towel' or 'plant'."""
    root = empty(name, origin, rot_z)
    box(f"{name}_bottom", x0, x0 + w, -d, 0, z0, z0 + t, "wood", root, bevel=0.05)
    box(f"{name}_top", x0, x0 + w, -d, 0, z0 + h - t, z0 + h, "wood", root, bevel=0.05)
    box(f"{name}_left", x0, x0 + t, -d, 0, z0 + t, z0 + h - t, "wood", root, bevel=0.05)
    box(f"{name}_right", x0 + w - t, x0 + w, -d, 0, z0 + t, z0 + h - t, "wood", root, bevel=0.05)
    if prop == "towel":
        cylinder(f"{name}_towel", 1.8, w - 2.5, "towel", (x0 + w / 2, -d / 2, z0 + t + 1.8),
                 rot=(0, math.pi / 2, 0), parent=root)
    elif prop == "plant":
        cylinder(f"{name}_pot", 1.6, 3.0, "pot", (x0 + w / 2, -d / 2, z0 + t + 1.5), parent=root)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.4 * IN)
        pl = mesh_obj(f"{name}_plant", bm, "leaves", root, smooth=True)
        pl.location = I(x0 + w / 2, -d / 2, z0 + t + 5.0)
    return root


def _vine_mats():
    _mat("vine_leaf", (0.05, 0.20, 0.035), 0.3)           # glossy pothos green
    _mat("vine_leaf_lt", (0.16, 0.30, 0.05), 0.35)        # variegated, lighter leaves
    _mat("soil", (0.05, 0.035, 0.025), 0.95)


def wall_planter(name, origin, rot_z, z0, w=24, d=6, h=6, t=0.75, vines=9, seed=5):
    """Wall-mounted wood planter trough with a fluted front, filled with trailing vines.
    x from 0..w."""
    _vine_mats()
    rnd = random.Random(seed)
    root = empty(name, origin, rot_z)
    box(f"{name}_bottom", 0, w, -d, 0, z0, z0 + t, "wood", root, bevel=0.05)
    box(f"{name}_back", 0, w, -t, 0, z0 + t, z0 + h, "wood", root, bevel=0.05)
    box(f"{name}_front", 0, w, -d, -d + t, z0 + t, z0 + h, "wood", root, bevel=0.05)
    box(f"{name}_end_l", 0, t, -d + t, -t, z0 + t, z0 + h, "wood", root, bevel=0.05)
    box(f"{name}_end_r", w - t, w, -d + t, -t, z0 + t, z0 + h, "wood", root, bevel=0.05)
    n = 24
    for r in range(n):         # fluting on the front
        c = cylinder(f"{name}_reed", w / n * 0.42, h - 0.3, "wood", (w / n * (r + 0.5), -d - 0.02, z0 + h / 2),
                     segs=12, parent=root)
        c.scale = (1, 0.5, 1)
    box(f"{name}_soil", t, w - t, -d + t, -t, z0 + t, z0 + h - 0.8, "soil", root)

    def leaf(pos, size, mat):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=size * IN)
        lf = mesh_obj(f"{name}_leaf", bm, mat, root, smooth=True)
        lf.location = I(*pos)
        lf.scale = (1.0, 0.28, 0.8)
        lf.rotation_euler = (rnd.uniform(-0.6, 0.6), rnd.uniform(-0.5, 0.5), rnd.uniform(0, math.pi))

    # a low mound of leaves over the soil
    for k in range(40):
        p = (rnd.uniform(1.5, w - 1.5), rnd.uniform(-d + 1.2, -1.2), z0 + h - 0.4 + rnd.uniform(0, 2.2))
        leaf(p, rnd.uniform(1.0, 1.5), "vine_leaf" if rnd.random() < 0.7 else "vine_leaf_lt")
    # vines spill over the front edge and hang down, drifting slightly
    for v in range(vines):
        x = rnd.uniform(2, w - 2)
        length = rnd.uniform(10, 30)
        drift = rnd.uniform(-4, 4)
        steps = int(length / 1.6)
        for k in range(steps):
            f = k / max(steps - 1, 1)
            px = x + drift * f + rnd.uniform(-0.4, 0.4)
            py = -d - 0.8 - 1.2 * math.sin(f * math.pi * 0.5) + rnd.uniform(-0.3, 0.3)
            pz = z0 + h + 0.5 - f * length
            leaf((px, py, pz), rnd.uniform(0.8, 1.25) * (1 - 0.3 * f), "vine_leaf" if rnd.random() < 0.7 else "vine_leaf_lt")
    return root


def planter_cube(name, origin, rot_z, z0, w=24, d=6, h=24, t=0.75, ph=6, seed=7, mid=True, led=False):
    """Planter + open cube in one wood unit. The bottom compartment is the planter
    (fluted front lip ph tall, soil, vines spilling over the front and hanging below);
    above it a middle shelf (mid) and an open top compartment; led: warm strip under the top."""
    _vine_mats()
    rnd = random.Random(seed)
    root = empty(name, origin, rot_z)
    zt = z0 + h
    zm = z0 + h / 2                                  # middle shelf
    box(f"{name}_bottom", 0, w, -d, 0, z0, z0 + t, "wood", root, bevel=0.05)
    box(f"{name}_top", 0, w, -d, 0, zt - t, zt, "wood", root, bevel=0.05)
    box(f"{name}_side_l", 0, t, -d, 0, z0 + t, zt - t, "wood", root, bevel=0.05)
    box(f"{name}_side_r", w - t, w, -d, 0, z0 + t, zt - t, "wood", root, bevel=0.05)
    if mid:
        box(f"{name}_mid", t, w - t, -d, 0, zm - t / 2, zm + t / 2, "wood", root, bevel=0.05)
    if led:    # warm LED strip tucked under the top board's front edge, washing down over the plants
        box(f"{name}_led", t + 0.3, w - t - 0.3, -d + 0.4, -d + 1.0, zt - t - 0.12, zt - t, "led_strip", root)
        ld = bpy.data.lights.new(f"{name}_ledlight", "AREA")
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = (w - 2 * t) * IN, 0.6 * IN
        ld.energy = 1.5                                # soft accent glow, not a wash
        ld.color = (1.0, 0.82, 0.6)
        lo = bpy.data.objects.new(f"{name}_ledlight", ld)
        lo.location = I(w / 2, -d + 0.7, zt - t - 0.2)
        link(lo, root)                                 # area lights point down (-z) by default
    # planter in the bottom compartment: back panel only as tall as the planter box, so the
    # wall shows through the open frame
    box(f"{name}_pback", t, w - t, -t, 0, z0 + t, z0 + ph, "wood", root, bevel=0.05)
    box(f"{name}_pfront", t, w - t, -d, -d + t, z0 + t, z0 + ph, "wood", root, bevel=0.05)
    n = 22
    for r in range(n):
        c = cylinder(f"{name}_reed", (w - 2 * t) / n * 0.42, ph - t - 0.3, "wood",
                     (t + (w - 2 * t) / n * (r + 0.5), -d - 0.02, z0 + (t + ph) / 2), segs=12, parent=root)
        c.scale = (1, 0.5, 1)
    box(f"{name}_soil", t, w - t, -d + t, -t, z0 + t, z0 + ph - 0.8, "soil", root)
    if mid:    # props in the top compartment
        cylinder(f"{name}_towel", 1.9, 9, "towel", (6.5, -d / 2, zm + t / 2 + 1.9), rot=(0, math.pi / 2, 0), parent=root)
        cylinder(f"{name}_candle", 1.4, 3.2, "pot", (w - 5, -d / 2, zm + t / 2 + 1.6), parent=root)

    def leaf(pos, size, mat):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=size * IN)
        lf = mesh_obj(f"{name}_leaf", bm, mat, root, smooth=True)
        lf.location = I(*pos)
        lf.scale = (1.0, 0.28, 0.8)
        lf.rotation_euler = (rnd.uniform(-0.6, 0.6), rnd.uniform(-0.5, 0.5), rnd.uniform(0, math.pi))

    top_soil = z0 + ph - 0.8
    grow = min(4.5, zm - t - top_soil - 1.2) if mid else (zt - t - top_soil - 2.5)   # taller inside an open frame
    for k in range(40 if mid else 75):    # foliage filling the planter compartment
        leaf((rnd.uniform(1.8, w - 1.8), rnd.uniform(-d + 1.0, -1.2),
              top_soil + rnd.uniform(0.3, 0.3 + grow * rnd.random() ** 1.4)),
             rnd.uniform(1.0, 1.4), "vine_leaf" if rnd.random() < 0.7 else "vine_leaf_lt")
    for v in range(9):         # vines spill over the fluted lip and hang below the unit
        x = rnd.uniform(2, w - 2)
        length = rnd.uniform(10, 30)
        drift = rnd.uniform(-4, 4)
        steps = int(length / 1.6)
        for k in range(steps):
            f = k / max(steps - 1, 1)
            px = x + drift * f + rnd.uniform(-0.4, 0.4)
            py = -d - 0.8 - 1.2 * math.sin(f * math.pi * 0.5) + rnd.uniform(-0.3, 0.3)
            leaf((px, py, z0 + ph + 0.5 - f * length), rnd.uniform(0.8, 1.25) * (1 - 0.3 * f),
                 "vine_leaf" if rnd.random() < 0.7 else "vine_leaf_lt")
    return root


# ---------------------------------------------------------------- outside
def black_walnut(tx, ty, gz, trunk_r):
    """A black walnut outside a window: the trunk and a few scaffold limbs (what shows through
    the glass). gz: ground height relative to the room floor."""
    rnd = random.Random(7)
    bark_material()
    leaf_material()
    tr = trunk_r
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=tr * IN, radius2=tr * 0.55 * IN, depth=260 * IN)
    trunk = mesh_obj("tree_trunk", bm, "bark", smooth=True)
    trunk.location = I(tx, ty, gz + 130)
    for k in range(3):
        ang = rnd.uniform(0, 2 * math.pi)
        z0 = rnd.uniform(160, 260)
        length = rnd.uniform(90, 150)
        lean = rnd.uniform(0.6, 1.0)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=tr * 0.42 * IN, radius2=1.2 * IN, depth=length * IN)
        limb = mesh_obj("tree_limb", bm, "bark", smooth=True)
        d = Vector((math.cos(ang) * lean, math.sin(ang) * lean, 1.0)).normalized()
        limb.location = I(*(Vector((tx, ty, gz + z0)) + d * (length / 2)))
        limb.rotation_euler = d.to_track_quat("Z", "Y").to_euler()


def treeline(gz, x0=-900, x1=1100, y0=950, y1=1250, n=26, seed=11):
    """Distant tree line (soft green blobs) so the lawn doesn't run flat to the horizon."""
    principled("treeline", (0.05, 0.09, 0.035), 0.9)
    rnd = random.Random(seed)
    for k in range(n):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=3, radius=rnd.uniform(140, 240) * IN)
        t = mesh_obj("treeline", bm, "treeline", smooth=True)
        t.location = I(rnd.uniform(x0, x1), rnd.uniform(y0, y1), gz + rnd.uniform(120, 220))
        t.scale = (1.3, 1, rnd.uniform(0.8, 1.2))
