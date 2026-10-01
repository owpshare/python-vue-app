#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE_DIR="$ROOT_DIR/.deploy-package"
ZIP_PATH="$ROOT_DIR/.deploy-package.zip"

rm -rf "$STAGE_DIR" "$ZIP_PATH"
mkdir -p "$STAGE_DIR"

# for item in app.py calculator.py requirements.txt startup.sh; do
#   if [[ -e "$ROOT_DIR/$item" ]]; then
#     cp "$ROOT_DIR/$item" "$STAGE_DIR/"
#   fi
# done

# if [[ -d "$ROOT_DIR/dist" ]]; then
#   cp -R "$ROOT_DIR/dist" "$STAGE_DIR/"
# fi

tar -cf - dist server app.py requirements.txt startup.sh | tar -xf - -C "$STAGE_DIR"

find "$STAGE_DIR" -type d \( -name __pycache__ -o -name .git -o -name .venv -o -name .vscode \) -prune -exec rm -rf {} +
find "$STAGE_DIR" -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.log' \) -delete

(
  cd "$STAGE_DIR"
  zip -qr "$ZIP_PATH" .
)

echo "Deployment package created: $ZIP_PATH"
echo "Package contents:"
find "$STAGE_DIR" -maxdepth 2 -mindepth 1 | sort
