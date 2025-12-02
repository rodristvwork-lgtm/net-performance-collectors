#!/bin/bash

# kill wget.py if running
pgrep -f ping.py | xargs kill -9 2>/dev/null

# current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv in current shell
source "$SCRIPT_DIR/.venv/bin/activate"

# change where file is located:
cd ping

# Run directory
python ping.py

# deactivate virtual environment
deactivate

# back to main directory
cd ..
