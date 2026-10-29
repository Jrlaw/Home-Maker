"""Room dimensions: one standard file per room, houses/<house>/rooms/<room>/dimensions.json.

A room's layout.py declares each size someone may want to check or correct with

    KITCHEN_W = dimension("kitchen_w", 109, "plan", "back of the west run to the east wall")

and uses the returned value as before. When dimensions.json has that name with
"override": true (typed into the walkthrough, or by hand), its value wins over the default in
the code. Every export rewrites the file with all of the room's dimensions, so it also serves
as the room's size sheet:

    {"units": "inches",
     "dimensions": {"kitchen_w": {"value": 109, "src": "plan", "note": "...",
                                  "default": 109, "override": false, "updated": null}}}

src says where a number came from, the same words the Plans page uses: measured, plan, photo,
design (a chosen new size) or assumed. Dimension lines drawn with core.dim(..., key=name) are
tied to a dimension, so the walkthrough can show and edit it.
"""
import json
import os
import sys

FILE = "dimensions.json"
SOURCES = ("measured", "plan", "photo", "design", "assumed")
REG = {}          # name -> entry, as declared this run (with any override applied)
_files = {}       # dimensions.json path -> its "dimensions" dict as loaded


def _read(path):
    if path not in _files:
        try:
            with open(path) as f:
                _files[path] = json.load(f).get("dimensions", {})
        except (OSError, ValueError):
            _files[path] = {}
    return _files[path]


def dimension(name, default, src, note=""):
    """A named size in inches; returns the hand-set value from dimensions.json if there is one."""
    caller = sys._getframe(1).f_globals.get("__file__", "")
    path = os.path.join(os.path.dirname(os.path.abspath(caller)), FILE)
    saved = _read(path).get(name, {})
    over = bool(saved.get("override"))
    REG[name] = dict(value=saved["value"] if over else default,
                     src=saved.get("src", src) if over else src,
                     note=saved.get("note", note) if over else note,
                     default=default, override=over, updated=saved.get("updated") if over else None,
                     _path=path)
    return REG[name]["value"]


def entries():
    """The declared dimensions for scene.json (without the file paths)."""
    return {k: {f: v for f, v in e.items() if not f.startswith("_")} for k, e in REG.items()}


def write():
    """Rewrite each room's dimensions.json with everything declared this run."""
    by_path = {}
    for k, e in REG.items():
        by_path.setdefault(e["_path"], {})[k] = {f: v for f, v in e.items() if not f.startswith("_")}
    for path, dims in by_path.items():
        with open(path, "w") as f:
            json.dump({"units": "inches", "dimensions": dict(sorted(dims.items()))}, f, indent=1)
            f.write("\n")


def set_override(path, name, value, src, note, updated):
    """Record a hand-set value (used by the local server when the walkthrough saves an edit)."""
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {"units": "inches", "dimensions": {}}
    e = data.setdefault("dimensions", {}).setdefault(name, {})
    e.update(value=value, src=src, note=note, override=True, updated=updated)
    e.setdefault("default", value)
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
