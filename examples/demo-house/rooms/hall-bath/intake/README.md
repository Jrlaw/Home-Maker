# Intake: Hall bath

The example room has one photo and no tape measure, the hardest case the process handles. Every
size comes from the photo, scaled by things of known size.

## Photos

| Photo | What it shows |
|---|---|
| `nps-before.jpg` | From the doorway, looking north: wall-hung sink and medicine cabinet (west wall), the stub wall with a plumbing access panel, the tub alcove with a blue curtain, the toilet under the window. Copied to `web/before/photo1.jpg`. |

**Source:** "Seasonal employee housing bathroom before renovation", Yellowstone National Park
(NPS / Jacob W. Frank), 9 June 2020. Public domain (a work of the U.S. federal government).
https://commons.wikimedia.org/wiki/File:Seasonal_employee_housing_bathroom_before_renovation_(50014558717).jpg

## Measurements

All FROM PHOTO, in inches. The scale comes from the 4-1/4" wall tiles (counted course by
course), a standard 60" x 30" alcove tub, and an 80" door.

| What | Measurement | How |
|---|---|---|
| Ceiling height | 96 | guess (8 ft, the top isn't in the photo) |
| Room, east-west | 66 | photo: tub 30" + the toilet bay |
| Room, north-south | 96 | photo: tub 60" + the 4-1/2" stub wall + the sink bay |
| Tile wainscot | 49 to the cap | photo: 11 courses of 4-1/4" over a 2" cove base |
| Window (north wall) | 24 W x 38 H, sill at 52, 39 from the west wall | photo |
| Door (south wall) | 28 x 80, 18 from the west wall, swings in, hinged east | photo |
| Toilet | center 51 from the west wall | photo |
| Sink | 20 W x 17 D, rim at 33, centered 77 from the north wall | photo |
| Medicine cabinet | 18 W x 24 H, bottom at 52 | photo |

**Model check:** `./render.sh --design before --cams photo1` lines up with the photo to within a
tile or two. The camera was fitted to the photo's corners and tile lines (heading about 27°
west of north, tilted down 12°, a 12.5 mm lens on a 36 mm frame).

## Floor plan / listing

- None.

## Notes from the walkthrough

- "North" is the wall across from the door (the toilet and window wall).
- Stays: the tub, the window, the door. Everything else is replaced.
- Q: Will a standard vanity fit where the sink is? A: The sink bay is 31-1/2" (96 - 60 - 4-1/2),
  so a 30" vanity fits with about 1" to spare. Tape it before ordering.
