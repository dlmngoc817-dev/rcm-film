#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then python3 -m venv .venv; fi
if [ ! -f .venv/.rcm-installed ]; then
  .venv/bin/python -m pip install -r requirements.txt
  touch .venv/.rcm-installed
fi
exec .venv/bin/python -m streamlit run app.py
