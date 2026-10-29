# Home renders

Photoreal 3D models of rooms, before and after a remodel, with a walkthrough you can open in the
browser. One room at a time, in any house.

**Claude Code runs this project.** You talk; Claude does the modeling, rendering and
bookkeeping. Send it photos, measurements, product links and ideas, and it builds the room in
Blender, renders options side by side, and records every choice. You don't need to run any of
the scripts yourself.

## Getting started

1. Install [Claude Code](https://claude.com/claude-code) and
   [Blender](https://www.blender.org/download/) (4.2 or newer, in its default location).
   You also need Python 3 and Git. On Windows, use WSL or Git Bash.
2. Clone this repo, open a terminal in it, and run `claude`.
3. Say **"set me up"**. Claude checks that Blender renders (and on which GPU), then creates a
   private `houses/` folder for your rooms. It's its own repo, so your photos and renders never
   go into this shared one.
4. Say **"new room: &lt;house&gt;, &lt;room&gt;"** (for example "new room: ours, kitchen"). Claude
   gives you a short list of photos to take and things to measure.

## Talking to it

- **Photos, measurements, a floor plan:** drop them in. Claude models the room as it is today
  and checks the model against your photos before designing anything.
- **Ideas and products:** paste a link or describe it ("what would sage paint look like?").
  Claude logs it in the room's selections list, models it, and renders it next to the other
  options.
- **Decisions:** "go with the blue tile." Claude makes it the default and keeps the passed-on
  options with the reason.
- **"continue &lt;room&gt;":** where the room stopped and what's next.
- **"status":** every room and its next step.
- **"show me the walkthrough":** Claude starts the local viewer and gives you the link
  (http://127.0.0.1:8000). There you can walk around in 3D, switch day and evening, compare
  designs and fix a measurement.

## How it works

Claude follows [PROCESS.md](PROCESS.md) (start → intake → model the room as it is → ideas and
selections → renders and walkthrough → save), with the `room` skill in `.claude/skills/room/`.
For the curious:

- `houses/<house>/rooms/<room>/`: one room. Photos and notes (`intake/`), every product and
  idea (`selections.md`), the model (`layout.py`, `room.py`), renders, and the walkthrough
  (`web/`).
- `template/`: what a new room or house starts from.
- `lib/`: shared by every room. `roomkit/` has the Blender building blocks, `web/` the
  walkthrough viewer, `tools/` small helpers, and `render.sh` finds Blender and the GPU.
