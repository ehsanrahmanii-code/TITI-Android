"""TITI stub — real dashboard comes from LLL/TITAN_PRO_V75_PWA.py (loaded by titan_boot)."""
from __future__ import annotations

# Intentionally NO Flask shell page.
# If this module is imported as fallback, boot will raise ENGINE_MISSING.

def run_titan(open_browser: bool = False):
    raise RuntimeError(
        "ENGINE_MISSING: put TITAN_PRO_V75_PWA.py in /storage/emulated/0/LLL/ "
        "and grant All files access, then reopen TITI"
    )
