#!/usr/bin/env bash
set -euo pipefail
echo "== TITI engine prepare (full V75) =="
PY=app/src/main/python
mkdir -p "$PY"
cd "$PY"

if ls engine.part* >/dev/null 2>&1; then
  echo "Found parts: $(ls engine.part* | wc -l)"
  cat engine.part* > /tmp/titi_engine.b64
  python3 - <<'PY'
import base64, gzip, pathlib
b64 = pathlib.Path("/tmp/titi_engine.b64").read_text(encoding="ascii").replace("\n","").replace(" ","")
raw = gzip.decompress(base64.b64decode(b64))
out = pathlib.Path("titan_engine.py")
out.write_bytes(raw)
print("decoded titan_engine.py bytes=", len(raw))
assert len(raw) > 500_000, "engine too small"
assert b"Flask" in raw or b"run_titan" in raw
print("sanity OK")
PY
else
  echo "ERROR: no engine.part* files"
  exit 1
fi

test -f titan_engine.py
test -f titan_boot.py
wc -c titan_engine.py
echo "full engine ready"
