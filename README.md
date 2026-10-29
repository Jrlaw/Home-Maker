# Home renders

Photoreal 3D models of rooms, before and after a remodel, with a walkthrough you can open in the
browser. One room at a time, in any house.

**Claude Code runs this project.** You talk; Claude does the modeling, rendering and
bookkeeping. Send it photos, measurements, product links and ideas, and it builds the room in
Blender, renders options side by side, and records every choice. You don't need to run any of
the scripts yourself.

[![A real session: one photo of a dated bathroom, real products, renders and the walkthrough](docs/demo.gif)](docs/demo.mp4)

*A real Claude Code session, sped up ([full video](docs/demo.mp4)). Starting from one
public-domain photo, Claude finds the products, models the room as it is and as redesigned,
renders the options, and builds the website. The result is the example room in
`examples/demo-house/rooms/hall-bath/`: open http://127.0.0.1:8000 and choose **Example**.*

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

## Viewing your rooms

Everything you look at is a web page served from your own machine:
**http://127.0.0.1:8000**. Ask Claude to "show me the walkthrough" and it starts the server
and gives you the link. To start it yourself, run `lib/serve.sh` in this folder and leave it
running.

- **Home:** every house and room, each with its latest render.
- **Walkthrough:** walk around the room in 3D. Switch day and evening, flip between designs,
  look at the before photos, and fix a measurement (Claude re-exports the room for you).
- **Plans:** a top-down view with every dimension and where it came from.
- **Selections:** every product and idea for the room, chosen or not, with links and prices.

The server only listens on this machine. You can also open a room's `web/index.html`
straight from the folder, but correcting dimensions needs the server.

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
- **"show me the walkthrough":** Claude starts the viewer and gives you the link (see
  above).

## Tips

- **Ask for an expert review.** Have Claude spawn a sub-agent that plays a trade and critiques
  the design, for example: *"Spawn an agent who is a cabinet designer and have them review our
  renderings and cabinet models for placement and usability in where they're located."* A
  lighting designer, electrician, tile setter or plumber catches different things: clearances,
  door swings, where the light falls, outlet and code rules. Ask for one whenever a part of the
  room gets settled, and log what comes back in `selections.md`.
- **Tape-measure what matters first.** A model built from photos is close but not exact. Before
  ordering anything, measure the sizes the design depends on (the walkthrough's Dimensions
  button shows which ones are guesses), type them into the walkthrough, and Claude rebuilds the room.
- **One question at a time.** "What would a darker grout look like?" gets a quick side-by-side.
  Many small asks are better than one big rewrite.
- **Send product links, not names.** Claude saves the photo and the spec sheet, so the model uses
  the real dimensions and the link still means something later.
- **Stop anywhere.** Say "let's stop here" and Claude writes down where the room stands and the
  next step; "continue &lt;room&gt;" picks it back up in a new session.

## Ideas to build on

- **Expert reviews as a standard step.** The trade reviews above have been useful enough to
  write into `PROCESS.md`: a cabinet designer once the layout is set, a lighting designer
  before the lights are picked, and a contractor's walk-through before anything is ordered.
- **A whole-house walkthrough** once two connected rooms are modeled (see `PROCESS.md`, Houses).

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
