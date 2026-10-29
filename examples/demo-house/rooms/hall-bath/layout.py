"""Hall bath layout: every dimension, in inches.

Plan coordinates: x runs east, y runs north, and the interior face of the north wall is y = 0,
so the room sits at negative y. Origin is the room's interior NW corner. "North" is the wall
across from the door (the toilet and window wall in the photo).

Tag every number with where it came from, so guesses are easy to find and replace:
  MEASURED    tape measure
  FROM PLAN   a listing plan, blueprint or scan
  FROM PHOTO  estimated from a photo against something of known size
  ASSUMED     a guess (standard size, or just a placeholder)
  DESIGN      a choice for the new design

The repo's example room: one photo and no tape measure (intake/README.md), so the sizes come
from the photo, scaled by the 4-1/4" wall tiles, a standard 60" x 30" tub and an 80" door.

Main sizes use dimension(): they're listed in dimensions.json, shown in the walkthrough and
can be corrected there (a hand-set value overrides the default here).
"""
from roomkit.dimensions import dimension

CEILING = 96                  # ASSUMED 8 ft
WALL_T = 4.5                  # ASSUMED interior wall (2x4 + drywall)

# --- Room -------------------------------------------------------------------------
ROOM_W = dimension("room_w", 66, "photo", "interior, east-west: tub 30\" + toilet bay")
ROOM_D = dimension("room_d", 96, "photo", "interior, north-south: tub 60\" + stub wall + sink bay")

# --- Tub alcove (NW corner) and the stub wall at its foot ----------------------------
TUB_L, TUB_W = 60, 30         # FROM PHOTO: a standard alcove tub fills the alcove
STUB_T = 4.5                  # FROM PHOTO: stub wall between the tub and the sink, 30" wide
TILE_TOP = dimension("tile_top", 49, "photo", "green tile wainscot height: 11 courses of 4-1/4\" over a 2\" cove base")
COVE = 2.0                    # FROM PHOTO: dark brown vinyl cove base under the tile
TILE_T = 0.375                # tile + mortar on the walls

# --- Openings ---------------------------------------------------------------------
# wall: N, E, S or W. at: from the wall's left corner (as you face the wall from inside) to
# the edge of the opening, not the trim. Windows: sill = floor to the bottom of the opening.
WINDOWS = [
    dict(wall="N", at=39, width=24, sill=52, height=38),     # FROM PHOTO: centered over the toilet
]
DOORS = [
    dict(wall="S", at=20, width=28, height=80, door=True),   # FROM PHOTO: 18" off the west wall; swings in, hinged east
]
CANS = []                     # FROM PHOTO: no ceiling light in view (a light over the mirror, out of frame)

# --- As it is today (all FROM PHOTO) ---------------------------------------------------
OLD_SINK = dict(width=20, depth=17, rim=33, thick=6)        # wall-hung china sink
OLD_SINK_Y = -77                                            # its center, along the west wall
OLD_CABINET = dict(width=18, height=24, depth=4.5, bottom=52)   # surface medicine cabinet
OLD_TOILET = dict(depth=28.5, rim=15, tank_h=29.5, tank_w=19, tank_d=8, bowl_w=14.5, bowl_len=17.5,
                  wall_gap=1.0, seat_up=True, mat="bone", seat_mat="bone")
TOILET_X = dimension("toilet_x", 51, "photo", "west wall to the toilet's center, under the window")
ACCESS_PANEL = dict(width=17, height=30, bottom=2)          # tub plumbing access in the stub wall

# --- New design (sizes from the spec sheets) -------------------------------------------
# Glacier Bay Highgate 30" vanity, Pearl Gray, GB30P2-PG: 30.25 W x 18.75 D x 32.89 H
# (assembled), white cultured marble top with an integrated sink.
VANITY = dict(width=30.25, depth=18.75, height=32.89, top_t=1.0, kick=3.5)
VANITY_S = dimension("vanity_from_south", 0.4, "design", "south wall to the vanity: the 31\" sink bay just fits it")
# Gatco Designer 5079LG frameless beveled oval mirror, 24" W x 32" H
MIRROR = dict(width=24, height=32, center=dimension("mirror_center", 58, "design", "floor to the mirror's center"))
# Kohler Cimarron K-3851 two-piece round-front toilet, 1.28 gpf (spec sheet: 30-1/2" deep,
# 27-1/4" to the tank top, 16-1/2" rim, tank 17-5/8" x 8-1/2", 10" rough-in, 1-1/4" off the wall)
NEW_TOILET = dict(depth=30.5, rim=16.5, tank_h=27.25, tank_w=17.625, tank_d=8.5, bowl_w=14.75,
                  bowl_len=17.5, wall_gap=1.25)
NEW_TILE_TOP = dimension("new_tile_top", 54, "design", "new wainscot: Cloe 2.5x8 to 54\"")

# --- Lights, fan and outlet (from the lighting designer's review, 2026-10-29; selections.md) ---
# Halo HLB4LSFS5 4" canless wafers, set to 2700 K / 600 lm; the one over the tub is in the wet
# zone (wet-listed). About 44" apart, 20"+ off the walls, none over the mirror.
NEW_CANS = [(15, -42), (48, -30), (42, -74)]                 # DESIGN: tub, toilet, entry
# Kichler 5337NIS 24" three-light bar, brushed nickel, glass down, centered over the mirror
VANITY_LIGHT = dict(width=24, plate_h=4.75, ext=8, bottom=77)   # DESIGN: 3" above the mirror
FAN = (15, -12)               # DESIGN: Panasonic WhisperCeiling DC FV-0511VQ1 over the tub (80 CFM)
OUTLET_Y = -93.5              # DESIGN: GFCI at the backsplash's south end, the far side from the tub
