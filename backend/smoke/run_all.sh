#!/usr/bin/env bash
# Run the full Phase 0 Fanar discovery + faithfulness suite.
# Requires: VPN/hotspot reaching api.fanar.qa, and backend/.venv with deps installed.
# Usage:  bash smoke/run_all.sh        (run from backend/)
set -u
cd "$(dirname "$0")/.."                       # -> backend/
PY="${PY:-.venv/bin/python}"

run () { echo; echo "########## $1 ##########"; "$PY" "smoke/$1" || echo ">> $1 FAILED"; }

run 00_list_models.py
run 00b_probe.py
run 01_chat_json.py
run 02_aura_tts.py
run 03_aura_stt.py
run 04_diwan.py
run 05_oryx_ig.py
run 10_faithfulness_gate.py

echo; echo "Done. Raw payloads in smoke/_out/ (gitignored)."
