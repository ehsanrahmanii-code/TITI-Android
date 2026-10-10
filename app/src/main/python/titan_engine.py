"""TITI embedded shell — full V75 loads from Internal Storage/LLL."""
from __future__ import annotations
import os, time
from flask import Flask, jsonify

app = Flask(__name__)
STARTED = time.time()
VERSION = "TITI-7.5.0"
HOME = os.environ.get("TITAN_HOME") or os.environ.get("HOME") or "."


def _page(up: float) -> str:
    return f"""<!doctype html>
<html lang="fa" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0f0a1a">
<title>TITI</title>
<style>
body{{margin:0;font-family:system-ui;background:#0f0a1a;color:#e9d5ff;padding:28px 18px}}
.logo{{width:88px;height:88px;border-radius:24px;margin:0 auto 16px;
background:radial-gradient(circle at 30% 30%,#f472b6,#a78bfa 50%,#7c3aed);
border:2.5px solid #f472b6;display:grid;place-items:center;
font-size:28px;font-weight:900;color:#0f0a1a;
box-shadow:0 0 32px #7c3aed88}}
h1{{text-align:center;color:#f472b6;margin:0 0 4px;font-size:34px;letter-spacing:2px}}
.sub{{text-align:center;color:#a78bfa;margin:0 0 24px;font-size:13px}}
.card{{background:#1a1025;border:1px solid #4c1d95;border-radius:16px;padding:16px;margin-bottom:14px}}
.kv{{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #2e1065;font-size:13px}}
.ok{{color:#34d399}} code{{background:#2e1065;padding:2px 8px;border-radius:6px;color:#f472b6;font-size:12px}}
a.btn{{display:block;text-align:center;background:linear-gradient(90deg,#7c3aed,#f472b6);color:#fff;text-decoration:none;
padding:12px;border-radius:12px;font-weight:700;margin-top:8px}}
</style></head><body>
<div class="logo">TITI</div>
<h1>TITI</h1>
<p class="sub">V75 · storage: LLL only</p>
<div class="card">
<div class="kv"><span>version</span><b class="ok">{VERSION}</b></div>
<div class="kv"><span>uptime</span><b>{up}s</b></div>
<div class="kv"><span>port</span><b>127.0.0.1:8080</b></div>
<div class="kv"><span>HOME</span><b>{HOME}</b></div>
</div>
<div class="card">
<p style="font-size:13px;line-height:1.85;color:#c4b5fd;margin:0 0 10px">
برای داشبورد کامل فایل موتور را اینجا بگذارید:<br><br>
<code>/storage/emulated/0/LLL/TITAN_PRO_V75_PWA.py</code><br><br>
سپس اپ را ببندید و دوباره باز کنید.
</p>
<a class="btn" href="/api/v75/status">API Status</a>
<a class="btn" href="/health" style="background:#2e1065;color:#c4b5fd">Health</a>
</div>
</body></html>"""


@app.get("/")
def home():
    return _page(round(time.time() - STARTED, 1))


@app.get("/health")
def health():
    return jsonify(ok=True, version=VERSION, uptime=round(time.time() - STARTED, 1), storage="LLL", app="TITI")


@app.get("/api/v75/status")
@app.get("/api/v62/status")
@app.get("/api/v61/status")
def status():
    return jsonify(
        ok=True,
        version=VERSION,
        build="7.5.0",
        app="TITI",
        mode="embedded_shell",
        storage="LLL",
        uptime=round(time.time() - STARTED, 1),
        home=HOME,
        hint="Place TITAN_PRO_V75_PWA.py in Internal Storage/LLL for full analytics",
    )


def run_titan(open_browser: bool = False):
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080, threads=4)
    except Exception:
        app.run(host="0.0.0.0", port=8080, threaded=True, use_reloader=False)


if __name__ == "__main__":
    run_titan()
