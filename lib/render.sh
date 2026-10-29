#!/bin/sh
# Build a room in Blender and render it (or export the walkthrough model).
# Usage: lib/render.sh <room>/room.py [--cams photo1,plan] [--samples N] [--res PX] [--night]
#        [--out DIR] [--export DIR] [--save] [--cpu] [room options...]
# Each room has a ./render.sh that calls this with its own room.py.
# Finds Blender in this order: $BLENDER, `blender` on PATH, the usual install spots on macOS and
# Windows (Git Bash / WSL), then the Flathub Blender (CPU only: its sandbox can't load the host's
# GPU libraries). The GPU itself is picked inside Blender (finish() in lib/roomkit/core.py).
room=$1
shift

find_blender() {
    [ -n "$BLENDER" ] && { echo "$BLENDER"; return; }
    command -v blender 2>/dev/null && return
    for b in /Applications/Blender.app/Contents/MacOS/Blender \
             "$HOME/Applications/Blender.app/Contents/MacOS/Blender" \
             /c/Program\ Files/Blender\ Foundation/Blender*/blender.exe \
             /mnt/c/Program\ Files/Blender\ Foundation/Blender*/blender.exe; do
        [ -x "$b" ] && { echo "$b"; return; }
    done
}
blender=$(find_blender)

if [ -z "$blender" ]; then
    if flatpak info org.blender.Blender >/dev/null 2>&1; then
        repo=$(cd "$(dirname "$0")/.." && pwd)
        exec flatpak run --filesystem=/tmp --filesystem="$repo" --command=blender org.blender.Blender -b \
            --python "$room" -- "$@"
    fi
    echo "Blender not found. Install it from https://www.blender.org/download/ or set BLENDER=/path/to/blender" >&2
    exit 1
fi

# Fedora's packaged Blender can ship an older OpenColorIO than its color config asks for (2.4 vs
# 2.5); a copy of the config marked 2.4 loads fine (same AgX views), kept in the cache next to
# links to the original LUTs
if [ "$(readlink -f "$blender" 2>/dev/null)" = /usr/bin/blender ] && [ -d /usr/share/blender ]; then
    src=$(ls -d /usr/share/blender/*/datafiles/colormanagement | tail -n 1)
    if grep -q '^ocio_profile_version: 2\.5' "$src/config.ocio" 2>/dev/null; then
        ocio="$HOME/.cache/home-render/ocio"
        mkdir -p "$ocio"
        for d in luts filmic icc; do ln -sfn "$src/$d" "$ocio/$d"; done
        sed 's/^ocio_profile_version: 2\.5/ocio_profile_version: 2.4/' "$src/config.ocio" > "$ocio/config.ocio"
        export OCIO="$ocio/config.ocio"
    fi
fi
exec "$blender" -b --python "$room" -- "$@"
