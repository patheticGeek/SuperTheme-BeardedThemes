#!/usr/bin/env bash
# Downloads the latest Bearded Themes GitHub release, lets you pick which
# theme variant to install, and runs its installer. This is the entry point
# for anyone who hasn't cloned the repo -- it needs only curl and unzip, no
# git, no Node, no Python.
#
# If you have a local checkout with themes/ already built (e.g. you're
# working on the pipeline itself), use ./install-dev.sh instead -- it
# installs straight from local files without downloading anything.
#
# Usage:
#   ./install.sh                    list variants in the latest release, ask which to install
#   ./install.sh --variant=<name>   install a specific variant non-interactively (see --list)
#   ./install.sh --all              install the SuperTheme (every variant) non-interactively
#   ./install.sh --list             print available variants from the latest release and exit
#
# Any other flag (--apply, --system, --with-plymouth, --theme=<slug>) is
# forwarded as-is to the downloaded install-dev.sh -- see its --help for
# what those do. --theme=<slug> only matters if you picked --all, to narrow
# down to one variant inside the SuperTheme bundle.
#
# If the repo is private, set GITHUB_TOKEN (or GH_TOKEN) to a token with
# read access -- GitHub's API returns a plain 404 for private repos to
# unauthenticated requests, same as a repo that doesn't exist.

set -euo pipefail

REPO="patheticGeek/SuperTheme-BeardedThemes"
API_URL="https://api.github.com/repos/$REPO/releases/latest"
TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"

if ! command -v curl >/dev/null 2>&1; then
    echo "error: curl is required" >&2
    exit 1
fi
if ! command -v unzip >/dev/null 2>&1; then
    echo "error: unzip is required" >&2
    exit 1
fi

VARIANT=""
LIST_ONLY=0
FORWARD_ARGS=()

for arg in "$@"; do
    case "$arg" in
        --variant=*) VARIANT="${arg#--variant=}" ;;
        --all) VARIANT="SuperTheme" ;;
        --list) LIST_ONLY=1 ;;
        --help|-h)
            sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) FORWARD_ARGS+=("$arg") ;;
    esac
done

curl_auth() {
    if [ -n "$TOKEN" ]; then
        curl -fsSL -H "Authorization: Bearer $TOKEN" "$@"
    else
        curl -fsSL "$@"
    fi
}

echo "==> Checking latest release of $REPO" >&2
RELEASE_JSON="$(curl_auth "$API_URL")"

# variant<TAB>asset-name<TAB>download-url for every .zip asset; variant is
# the asset filename with its trailing -<version>.zip stripped. Pairs each
# "name" line ending in .zip with the "browser_download_url" line that
# follows it inside the same asset object -- good enough since GitHub's
# release JSON is stable, pretty-printed, one field per line.
VARIANTS="$(echo "$RELEASE_JSON" | awk '
    /"name": *"[^"]*\.zip"/ {
        line = $0
        sub(/.*"name": *"/, "", line)
        sub(/\.zip".*/, "", line)
        full = line
        variant = line
        sub(/-[^-]+$/, "", variant)
        pending_full = full
        pending_variant = variant
        next
    }
    /"browser_download_url":/ && pending_variant != "" {
        line = $0
        sub(/.*"browser_download_url": *"/, "", line)
        sub(/".*/, "", line)
        print pending_variant "\t" pending_full ".zip\t" line
        pending_variant = ""
    }
')"

if [ -z "$VARIANTS" ]; then
    echo "error: no .zip assets found on the latest release of $REPO" >&2
    exit 1
fi

if [ "$LIST_ONLY" -eq 1 ]; then
    echo "Available variants:"
    echo "$VARIANTS" | cut -f1 | sed 's/^/  - /'
    exit 0
fi

if [ -z "$VARIANT" ]; then
    if [ ! -t 0 ]; then
        echo "error: no --variant=<name> given and not running interactively -- use --list to see options" >&2
        exit 1
    fi
    echo "Available variants:"
    i=1
    NAMES=()
    while IFS=$'\t' read -r variant _name _url; do
        echo "  $i) $variant"
        NAMES+=("$variant")
        i=$((i + 1))
    done <<< "$VARIANTS"
    read -rp "Install which variant? [1-$((i - 1))]: " CHOICE
    VARIANT="${NAMES[$((CHOICE - 1))]:-}"
fi

MATCH="$(echo "$VARIANTS" | awk -F'\t' -v v="$VARIANT" '$1 == v')"
if [ -z "$MATCH" ]; then
    echo "error: no variant named '$VARIANT' in the latest release -- use --list to see options" >&2
    exit 1
fi

ASSET_NAME="$(echo "$MATCH" | cut -f2)"
ASSET_URL="$(echo "$MATCH" | cut -f3)"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

echo "==> Downloading $ASSET_NAME" >&2
curl_auth "$ASSET_URL" -o "$WORK_DIR/$ASSET_NAME"

echo "==> Extracting" >&2
unzip -q "$WORK_DIR/$ASSET_NAME" -d "$WORK_DIR"

EXTRACTED_DIR="$(find "$WORK_DIR" -mindepth 1 -maxdepth 1 -type d | head -n1)"
if [ -z "$EXTRACTED_DIR" ] || [ ! -f "$EXTRACTED_DIR/install.sh" ]; then
    echo "error: extracted archive doesn't contain install.sh -- unexpected zip layout" >&2
    exit 1
fi
chmod +x "$EXTRACTED_DIR/install.sh"

echo "==> Running installer from $ASSET_NAME" >&2
"$EXTRACTED_DIR/install.sh" "${FORWARD_ARGS[@]}"
