#!/usr/bin/env bash
set -euo pipefail
echo "== TITI engine prepare =="
PY=app/src/main/python
ls -lh "$PY" || true
test -f "$PY/titan_engine.py"
test -f "$PY/titan_boot.py"
echo "shell engine ready"
