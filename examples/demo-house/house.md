# Demo house

The repo's example house: one room, modeled from a single public-domain photo. A real house
lists every room here and on the **whole-house map** (`web/index.html`), built from
`house_layout.py`.

## Rooms

Modeled rooms have a folder under `rooms/`; the rest are placeholders on the map.

| Room | Id | Listed size | Status |
|---|---|---|---|
| Hall bath | `hall-bath` | 5'6" x 8'0" (from the photo) | design chosen, walkthrough built |
| Hall | `hall` | | placeholder |
| Bedroom | `bedroom` | | placeholder |

## Placement

House coordinates: inches, x east, y north, origin at the hall bath's interior NW corner.

| Room | Its origin (interior NW corner) in house coordinates | Rotation | Connects to |
|---|---|---|---|
| Hall bath | (0, 0) | 0 | the hall, through its south door |
