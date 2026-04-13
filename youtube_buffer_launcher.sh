#!/bin/bash

# CASE 1 — IP passed as argument
if [ -n "$1" ]; then
    IP_ADDR="$1"
    IP_CASE="Case 1: Provided as argument"

# CASE 2 — Auto-detect local IP if no argument
elif hostname -I >/dev/null 2>&1; then
    IP_ADDR=$(hostname -I | awk '{print $1}')
    IP_CASE="Case 2: Auto-detected local IP"

# CASE 3 — Prompt user interactively
else
    read -rp "Enter target IP address: " IP_ADDR
    IP_CASE="Case 3: User entered interactively"
fi

# Final safety check
if [ -z "$IP_ADDR" ]; then
    echo "Error: No IP address available."
    exit 1
fi

echo "----------------------------------------"
echo "IP Address Selected: $IP_ADDR"
echo "Source: $IP_CASE"
echo "----------------------------------------"

# Kill existing python process if running     
pgrep -f youtube_API_collector.py | xargs -r kill -9 2>/dev/null

# Environment setup                           
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv
source "$SCRIPT_DIR/.venv/bin/activate"

# Change to working directory
cd "$SCRIPT_DIR/youtube_buffer_API"

# Run Python script with selected IP          
"$SCRIPT_DIR/.venv/bin/python" youtube_API_collector.py "$IP_ADDR"

# Cleanup                                     
deactivate

# Return to project root
cd "$SCRIPT_DIR"