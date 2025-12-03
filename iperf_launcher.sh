#!/bin/bash

# kill iperf.py if running
pgrep -f iperf.py | xargs -r kill -9 2>/dev/null

# current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv in current shell
source "$SCRIPT_DIR/.venv/bin/activate"

# change where file is located:
cd "$SCRIPT_DIR/iperf"

# Run directory
"$SCRIPT_DIR/.venv/bin/python" iperf.py

# deactivate virtual environment
deactivate