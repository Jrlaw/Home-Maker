# HOUSE NAME

A line about the house: floors, rough size, what's being worked on. Every room can go on the
**whole-house map** (`web/index.html`) before any are modeled: outline them in
`house_layout.py`, then rebuild the map (from the repo root):

    python3 lib/tools/house_map.py houses/<house>

## Rooms

Modeled rooms have a folder under `rooms/`; the rest are placeholders on the map.

| Room | Id | Listed size | Status |
|---|---|---|---|
| Kitchen | `kitchen` | 12'0" x 10'0" | placeholder |

## Placement

House coordinates: inches, x east, y north, origin at one room's interior NW corner. Once
two touching rooms are both modeled, record each one's origin and rotation here, and the
doorway that connects them.

| Room | Its origin (interior NW corner) in house coordinates | Rotation | Connects to |
|---|---|---|---|
