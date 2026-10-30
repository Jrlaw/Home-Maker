"""This person's catalog: the specific products and colors they've modeled, shared by every room
in houses/. lib/roomkit has the generic parts (a two-piece toilet, a shaker vanity); a particular
model (a TOTO Aquia, an Afhocomp vanity) goes here. Rooms import it with `import catalog`, which
adds the colors in materials.py to roomkit's tables.
"""
from . import materials  # noqa: F401
