"""TITI bootstrap — load full V75 from LLL, else embedded shell."""
from __future__ import annotations

import importlib.util
import os
import sys
import threading
import traceback
from pathlib import Path

_started = False
_lock = threading.Lock()
_status = {"ok": False, "message": "idle", "error": None, "phase": "idle", "engine": None}


def status() -> dict:
    return dict(_status)


def _prepare_android_home() -> str:
    files = None
    try:
        from com.chaquo.python import Python  # type: ignore

        ctx = Python.getInstance().getPlatform().getApplication()
        files = str(ctx.getFilesDir().getAbsolutePath())
    except Exception:
        files = os.path.join(os.path.expanduser("~"), ".titi_files")

    home = None
    for cand in (
        "/storage/emulated/0/LLL",
        "/sdcard/LLL",
        "/storage/self/primary/LLL",
    ):
        try:
            os.makedirs(cand, exist_ok=True)
            probe = os.path.join(cand, ".titi_probe")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            home = cand
            break
        except Exception:
            continue
    if home is None:
        home = os.path.join(files, "LLL")
        for sub in ("", "secrets", "data", "cache", "memory"):
            os.makedirs(os.path.join(home, sub) if sub else home, exist_ok=True)

    os.environ["TITAN_HOME"] = home
    os.environ["TITAN_APP_HOME"] = home
    os.environ["HOME"] = home
    os.environ["TITAN_OPEN_BROWSER"] = "0"
    os.environ["TITAN_HOST"] = "0.0.0.0"
    os.environ["TITAN_PORT"] = "8080"
    os.environ["TITAN_PORT_DEFAULT"] = "8080"
    sys.dont_write_bytecode = True
    return home


def _load_full_engine(home: str):
    names = (
        "TITAN_PRO_V75_PWA.py",
        "TITAN_PRO_V75.py",
        "titan_engine_full.py",
        "titan.py",
    )
    roots = [Path(home), Path(home) / "engine", Path(home) / "data"]
    for root in roots:
        for name in names:
            path = root / name
            try:
                if path.is_file() and path.stat().st_size > 100_000:
                    spec = importlib.util.spec_from_file_location("titan_engine_full", str(path))
                    if spec is None or spec.loader is None:
                        continue
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules["titan_engine_full"] = mod
                    spec.loader.exec_module(mod)
                    return mod, str(path)
            except Exception:
                continue
    return None, None


def start_server() -> str:
    global _started
    with _lock:
        if _started:
            return str(_status.get("phase") or "already")
        _started = True
        _status.update({"ok": False, "message": "starting", "error": None, "phase": "boot"})

    def _run():
        try:
            _status["phase"] = "home"
            home = _prepare_android_home()
            _status["message"] = f"LLL:{home}"

            _status["phase"] = "import"
            full, eng_path = _load_full_engine(home)
            if full is not None:
                te = full
                _status["engine"] = f"full:{eng_path}"
                _status["message"] = f"full {eng_path}"
            else:
                import titan_engine as te

                _status["engine"] = "shell"
                _status["message"] = "shell — put V75 in LLL for full"

            _status["phase"] = "serve"
            if hasattr(te, "run_titan"):
                te.run_titan(open_browser=False)
            elif hasattr(te, "app"):
                try:
                    from waitress import serve

                    serve(te.app, host="0.0.0.0", port=8080, threads=6, channel_timeout=120)
                except Exception:
                    te.app.run(host="0.0.0.0", port=8080, threaded=True, use_reloader=False)
            else:
                raise RuntimeError("no run_titan")
            _status["ok"] = True
            _status["phase"] = "stopped"
        except Exception as exc:
            _status["ok"] = False
            _status["error"] = f"{exc}\n{traceback.format_exc()}"
            _status["message"] = "error"
            _status["phase"] = "error"

    threading.Thread(target=_run, name="titi-v75", daemon=True).start()
    return "booting"


def get_status_text() -> str:
    s = status()
    if s.get("error"):
        return "error: " + str(s["error"])[:400]
    return f"{s.get('phase')}: {s.get('message')} [{s.get('engine') or ''}]"
