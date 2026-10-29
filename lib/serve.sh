#!/bin/sh
# Serve every house and room on http://127.0.0.1:8000 (this machine only). lib/serve.py also
# saves sizes typed into a walkthrough (dimensions.json) and re-exports that room.
exec python3 "$(dirname "$0")/serve.py" "$@"
