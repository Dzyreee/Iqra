"""One-click backend launcher for IQRA.

Press ▶ Run in VS Code (or `python main.py`) to start the FastAPI server on
http://localhost:8000 with auto-reload — no need to remember the uvicorn command.

Requirements (one time):
  - Select the venv interpreter in VS Code (the one at backend/.venv).
  - pip install -r requirements.txt
  - Put your Fanar key in backend/.env  (FANAR_API_KEY=...) and connect the VPN.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Run from this folder so the `app` package imports no matter where Run is pressed.
HERE = Path(__file__).resolve().parent
os.chdir(HERE)
sys.path.insert(0, str(HERE))

if __name__ == "__main__":
    import uvicorn

    print("▶ IQRA backend → http://localhost:8000   (Ctrl+C to stop)")
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)
