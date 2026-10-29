---
name: room
description: 3D room models for home remodels (Blender renders + browser walkthrough), one room at a time in any house. Use when the user says "set me up" (first run), wants to start a new room ("new room: ours, kitchen"), continue or update a modeled room, share photos/measurements/product links for a room, compare options (tile, paint, lights), or record a choice.
argument-hint: "[new <house> <room> | continue <room> | status]"
---

# Room models

Everything lives in this repo. The toolkit (`lib/`, `template/`, the docs) is shared; the
user's houses live in `houses/`, their own private repo, which this repo ignores.
**Read `PROCESS.md` first, every time.** It is the playbook: start → intake → model the room as
it is → ideas and selections → standard renders and walkthrough → save and stop. Then read the
room's `README.md` ("Current state" says where it stopped) and `selections.md`.

The user drives everything by talking; never hand them commands to run. Run renders, exports,
the selections page and the local server (`lib/serve.sh`, http://127.0.0.1:8000) yourself.

**First run ("set me up", or `houses/` doesn't exist):**
1. Check Blender: copy `template/room/` to a temp folder inside `houses/_check/rooms/box`, run its
   `./render.sh --cams photo1 --samples 16 --res 800 --out /tmp/home-render-check`, and report
   the `RENDER DEVICE` line (none means CPU: say renders will be slow). If Blender isn't found,
   say where to install it or set `BLENDER=/path/to/blender`. Delete `houses/_check` after.
2. Create the private houses repo: `git init houses`, copy `template/home.html` to
   `houses/index.html`, and write `houses/.gitignore` with: `*/rooms/*/renders/*.jpg`,
   `*/rooms/*/web/bundle.js`, `*/rooms/*/web/.bake/`, `*.blend`, `*.blend1`, `__pycache__/`.
   Offer to connect it to a private remote of their own.
3. Ask for their first room ("new room: <house>, <room>").

## Commands

- **new `<house>` `<room>`:** PROCESS.md step 0. Copy `template/room/` to
  `houses/<house>/rooms/<room>/` (and `template/house/` for a new house), add the room to
  `house.md` and `houses/index.html`, and give the user the shot list and measurement sheet
  from the room's `intake/README.md` (short, numbered, including the "no floor plan" option).
- **continue `<room>`:** read the room's README "Current state" and selections.md "Open
  decisions", say where it stopped in two or three lines, and offer the next step.
- **status:** list the houses and rooms, each with its status line and next step.

## Rules that matter most

- **Log every product, link, suggestion and choice in the room's `selections.md` as it happens.**
  Do this before modeling it. Passed-on options stay under "Considered" with the reason. Save
  product photos to `intake/products/`.
- **Tag every dimension** in `layout.py` MEASURED / FROM PLAN / FROM PHOTO / ASSUMED. With no
  floor plan, estimate from photos against known sizes, and ask for one or two specific
  measurements to settle conflicts.
- **Check the model against the photos** before designing: render each photo view and compare
  them side by side.
- **Shared parts:** reuse `lib/roomkit` and add general parts there. Keep one-offs in the room's
  `room.py`.
- **Rendering:** through the room's `./render.sh`, which finds Blender and the GPU. Time the
  first render on a machine and give ETAs from it.
- **Commits:** commit and push only when the user asks, with their own git identity. Room work
  goes in the `houses/` repo; toolkit changes (`lib/`, `template/`, docs) go in this repo.
- **Stopping:** end every stop by updating the room README's "Current state" with a small,
  concrete next step.
