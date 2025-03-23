#!/usr/bin/env sh

PROJECT_DIR=$(dirname "$(realpath "$0")")
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

echo "[entrypoint.sh] - $(date +%Y-%m-%dT%H:%M:%S.%3N%:z) - Starting API"
python -m api