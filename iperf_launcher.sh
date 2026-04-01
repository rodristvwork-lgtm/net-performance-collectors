#!/bin/bash

set -euo pipefail

# Optional defaults (can be overridden via env vars or CLI args)
SERVER_IP="${IPERF_SERVER_IP:-178.215.228.109}"
DURATION="${IPERF_DURATION:-20}"
START_PORT="${IPERF_START_PORT:-9212}"
END_PORT="${IPERF_END_PORT:-9240}"
BANDWIDTH="${IPERF_BANDWIDTH:-10M}"
UDP_UPLOAD_BANDWIDTH="${IPERF_UDP_UPLOAD_BANDWIDTH:-10M}"
UDP_DOWNLOAD_BANDWIDTH="${IPERF_UDP_DOWNLOAD_BANDWIDTH:-100M}"
SCENARIO="${IPERF_SCENARIO:-all}"
CONNECT_TIMEOUT_MS="${IPERF_CONNECT_TIMEOUT_MS:-3000}"
COMMAND_TIMEOUT_S="${IPERF_COMMAND_TIMEOUT_S:-35}"
SAVE_RESULTS="${IPERF_SAVE_RESULTS:-1}"

# Allow first positional argument as server IP for convenience
if [[ $# -gt 0 && "${1:0:1}" != "-" ]]; then
  SERVER_IP="$1"
  shift
fi

if [[ -z "$SERVER_IP" ]]; then
  echo "Errore: specifica il server iperf con IPERF_SERVER_IP o primo argomento."
  echo "Esempio: ./iperf_launcher.sh 178.215.228.109 --save"
  exit 1
fi

# kill previous iperf.py if running (gentle first, then force)
if pgrep -f "iperf.py" >/dev/null 2>&1; then
  pgrep -f "iperf.py" | xargs -r kill 2>/dev/null || true
  sleep 1
  pgrep -f "iperf.py" | xargs -r kill -9 2>/dev/null || true
fi

# current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${IPERF_OUTPUT_DIR:-$SCRIPT_DIR/results}"

# change where file is located:
cd "$SCRIPT_DIR/iperf"

# Select Python interpreter (prefer venv)
PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi

# Run iperf with defaults + extra user args
SAVE_FLAG=()
if [[ "$SAVE_RESULTS" == "1" || "$SAVE_RESULTS" == "true" || "$SAVE_RESULTS" == "TRUE" ]]; then
  SAVE_FLAG=(--save)
fi

echo "Output directory: $OUTPUT_DIR"
echo "Save results: ${SAVE_FLAG[*]:-disabled}"

"$PYTHON_BIN" iperf.py \
  --server-ip "$SERVER_IP" \
  --duration "$DURATION" \
  --start-port "$START_PORT" \
  --end-port "$END_PORT" \
  --bandwidth "$BANDWIDTH" \
  --udp-upload-bandwidth "$UDP_UPLOAD_BANDWIDTH" \
  --udp-download-bandwidth "$UDP_DOWNLOAD_BANDWIDTH" \
  --connect-timeout-ms "$CONNECT_TIMEOUT_MS" \
  --command-timeout-s "$COMMAND_TIMEOUT_S" \
  --scenario "$SCENARIO" \
  --output-dir "$OUTPUT_DIR" \
  "${SAVE_FLAG[@]}" \
  "$@"