#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt
"$PY" manage.py collectstatic --noinput
"$PY" manage.py migrate --noinput
