#!/bin/sh
# Convert iPhone HEIC photos to JPEG copies (1600 px, upright) next to the originals,
# so they can be viewed and compared with renders. Usage: lib/tools/heic2jpg.sh photo.HEIC ...
# ImageMagick and ffmpeg on this machine can't decode HEIC, so this uses pillow-heif in a
# small virtualenv kept in ~/.cache (created on first use).
venv="$HOME/.cache/home-render/heic-venv"
if [ ! -x "$venv/bin/python" ]; then
    python3 -m venv "$venv" && "$venv/bin/pip" install -q pillow-heif || exit 1
fi
exec "$venv/bin/python" -I "$(dirname "$0")/heic2jpg.py" "$@"
