"""Specific products, modeled from their spec sheets: `from catalog.parts import my_vanity`.
Same conventions as lib/roomkit/parts.py (inches; wall fixtures in a local frame with the wall
at y=0 and the room toward -y, turned onto a wall by rot_z), and the same helpers.
"""
import math  # noqa: F401

from roomkit import core  # noqa: F401
from roomkit.core import IN, box, cylinder, empty, prism  # noqa: F401
from roomkit.parts import _mat, egg, plan_prism  # noqa: F401
