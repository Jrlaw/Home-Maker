"""Paint and tile colors measured from products, added to roomkit's tables so any room can use
them by name (--tile-color <name>). Colors are linear RGB; tile colors are (darker, lighter),
and tiles vary between the two. Finishes: (roughness, strong tile-to-tile variation, wavy glaze).
"""
from roomkit.materials import PAINTS, TILE_COLORS, TILE_FINISHES

PAINTS.update({
    # "name": (r, g, b),   # brand and color name, where it was measured
})
TILE_COLORS.update({
    # "name": ((r, g, b), (r, g, b)),   # brand, line and color, size, finish ~#hex
})
TILE_FINISHES.update({
    # "name": (0.05, True, True),
})
