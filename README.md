# Home renders

Photoreal 3D models of rooms, before and after a remodel, built in Blender from a dimensions
file, with a walkthrough you can open in the browser. One room at a time, in any house.

It's built to be driven from Claude Code: you send photos, measurements and product links, and
Claude models the room, renders options and keeps track of every choice. You can also run it all
by hand.

## Setup

1. **Blender 4.2 or newer** ([blender.org/download](https://www.blender.org/download/)). It's
   found automatically on macOS (`/Applications/Blender.app`), Windows (the default install
   folder) and Linux (`blender` on the PATH, or the Flathub app). Anywhere else, set
   `BLENDER=/path/to/blender`. Renders use the GPU when Blender can see one (Metal, OptiX/CUDA,
   HIP or oneAPI), and the CPU otherwise.
2. **Python 3** for the local web server and the small tools in `lib/tools/` (standard library
   only).
3. **Optional:** [ImageMagick](https://imagemagick.org) (`magick`) for comparison sheets and the
   light-plan overlay. iPhone HEIC photos are converted by `lib/tools/heic2jpg.sh`, which sets up
   its own small Python environment (`pillow-heif`) on first use.
4. **Windows:** run the `.sh` scripts from Git Bash or WSL.
5. **Your houses:** create (or clone) your own private repo in `houses/`. This repo ignores that
   folder, so your rooms, photos and renders stay yours. See [houses/README.md](houses/README.md).

Check that rendering works with the template room:

    mkdir -p houses/test/rooms && cp -r template/room houses/test/rooms/box
    houses/test/rooms/box/render.sh --cams photo1 --samples 16 --res 800 --out /tmp/preview

The output names the render device (`RENDER DEVICE METAL [...]`, for example); no such line
means it rendered on the CPU. Delete `houses/test` afterwards.

## Using it with Claude Code

Open Claude Code in this folder. The `room` skill (`.claude/skills/room/`) comes with the repo,
so you can say:

- `new room: <house>, <room>`: starts a room and gives you the photo shot list and measurement
  sheet.
- `continue <room>`: says where the room stopped and what's next.
- Any photo, measurement or product link for a room: it's recorded in the room's files first,
  then modeled.

[PROCESS.md](PROCESS.md) is the playbook Claude follows, and is worth a read.

## What's here

- **[PROCESS.md](PROCESS.md):** how a room gets modeled, from photos and measurements to
  renders, options and decisions.
- **`houses/`:** your private houses repo (not part of this one): a folder per house, with
  `house.md` and `rooms/<room>/`, plus your home page `houses/index.html`.
- **`houses/<house>/rooms/<room>/`:** everything for one room:
  - `intake/`: photos, plan, measurements, notes.
  - `selections.md`: every product and idea, chosen or not, with links.
  - `layout.py` and `room.py`: the model.
  - `render.sh`: renders and the walkthrough export.
  - `renders/`, `web/`.
- **`template/room/`:** copied to start a new room. It renders a plain box room with a door,
  a window, a switch and a can light, ready to be reshaped. `template/home.html` starts
  `houses/index.html`.
- **`lib/`:** shared by every room.
  - `roomkit/`: Blender building blocks: walls, openings, materials, fixtures, products already
    modeled, render and export.
  - `web/`: the walkthrough viewer and the whole-house map (`housemap.js`).
  - `render.sh`: finds Blender and runs a room in it.
  - `serve.sh`: local web server.
  - `tools/`: HEIC conversion, a light-plan overlay, the whole-house map builder, the
    selections page.

## By hand

    cp -r template/room houses/<house>/rooms/<room>
    houses/<house>/rooms/<room>/render.sh --cams photo1,plan --samples 24 --res 1000 --out /tmp/preview

To view the walkthroughs, run `lib/serve.sh` and open http://127.0.0.1:8000. You can also
double-click a room's `web/index.html` once it's been exported (`./render.sh --export web`).
