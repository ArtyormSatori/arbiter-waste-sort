#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"

if [ -f "./venv/bin/python" ]; then
    PYTHON="./venv/bin/python"
else
    PYTHON="python3"
fi

echo "=========================================================="
echo " Starting WasteSense AI Server on http://${HOST}:${PORT}"
echo " Vision Model: watersplash/waste-classification (Edge CPU)"
echo " Track       : Arbiter Hacks V1 — Theme: Rethinking Waste"
echo "=========================================================="

exec "$PYTHON" -m uvicorn app.main:app --host "$HOST" --port "$PORT"
