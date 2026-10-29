# houses/

Your houses go here, and they never go into the shared toolkit repo (it ignores everything in
this folder except this file). Keep them in a private repo of your own, cloned or created right
here:

    git clone <your private repo> houses        # or: cd houses && git init

Inside it:

- `index.html`: your home page, a card per room (start from `../template/home.html`).
  `lib/serve.sh` opens it at http://127.0.0.1:8000.
- `<house>/house.md`: the house's rooms (and, optionally, `house_layout.py` for a whole-house
  map).
- `<house>/rooms/<room>/`: one room, copied from `../template/room/`.

Ignore these in your houses repo (renders are big and can be re-made):

    */rooms/*/renders/*.jpg
    */rooms/*/web/bundle.js
    */rooms/*/web/.bake/
    *.blend
    *.blend1
    __pycache__/
