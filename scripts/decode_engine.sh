#!/usr/bin/env bash
set -euo pipefail
echo "== TITI engine prepare =="
PY=app/src/main/python
test -f "$PY/titan_boot.py"
test -f "$PY/titan_engine.py"
echo "boot ready (full engine loads from device LLL at runtime)"
