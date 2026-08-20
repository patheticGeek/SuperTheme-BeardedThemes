#!/usr/bin/env bash
# Serves www/ locally for previewing the site, with docs/images/ linked in as
# www/images (which is gitignored -- CI copies it in the same way, see
# .github/workflows/pages.yml).
#
# Usage: ./scripts/serve-www.sh [port]     (default port 8000)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PORT="${1:-8000}"

if [ ! -e "$REPO_ROOT/www/images" ]; then
    ln -s ../docs/images "$REPO_ROOT/www/images"
fi

echo "==> Serving www/ at http://localhost:$PORT (Ctrl-C to stop)"
cd "$REPO_ROOT/www"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
