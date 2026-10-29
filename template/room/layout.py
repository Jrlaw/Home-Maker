"""ROOM NAME layout: every dimension, in inches.

Plan coordinates: x runs east, y runs north, and the interior face of the north wall is y = 0,
so the room sits at negative y. Origin is the room's interior NW corner. (If the room's
"north" isn't true north, say which wall is called north in README.md.)

Tag every number with where it came from, so guesses are easy to find and replace:
  MEASURED    tape measure
  FROM PLAN   a listing plan, blueprint or scan
  FROM PHOTO  estimated from a photo against something of known size
  ASSUMED     a guess (standard size, or just a placeholder)

Main sizes use dimension(): they're listed in dimensions.json, shown in the walkthrough and
can be corrected there (a hand-set value overrides the default here).
"""
from roomkit.dimensions import dimension

CEILING = 96                  # ASSUMED 8 ft
WALL_T = 4.5                  # ASSUMED interior wall (2x4 + drywall)

# --- Room -------------------------------------------------------------------------
ROOM_W = dimension("room_w", 144, "assumed", "interior, east-west")
ROOM_D = dimension("room_d", 120, "assumed", "interior, north-south")
# Not a rectangle? Replace these with an interior outline (clockwise from the NW corner), with
# a dimension(...) for each wall length, and build the walls from it in room.py.

# --- Openings ---------------------------------------------------------------------
# wall: N, E, S or W. at: from the wall's left corner (as you face the wall from inside) to
# the edge of the opening, not the trim. Windows: sill = floor to the bottom of the opening.
WINDOWS = [
    dict(wall="N", at=48, width=48, sill=30, height=48),     # ASSUMED
]
DOORS = [
    dict(wall="W", at=12, width=30, height=80, door=True),   # ASSUMED; door=False for a cased opening
]

# --- Lights and electrical ---------------------------------------------------------
CANS = [(ROOM_W / 2, -ROOM_D / 2)]          # ASSUMED one can in the middle; plan (x, y)
