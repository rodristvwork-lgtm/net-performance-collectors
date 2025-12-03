#!/bin/bash

# kill ping.py if running
pgrep -f ping.py | xargs -r kill -9 2>/dev/null

# current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv in current shell
source "$SCRIPT_DIR/.venv/bin/activate"

# change where file is located:
cd "$SCRIPT_DIR/ping"

# Run directory
"$SCRIPT_DIR/.venv/bin/python" ping.py

# deactivate virtual environment
deactivate