#!/usr/bin/env bash
# Build the BedrockOnLinux Flatpak.
#
#   scripts/build-flatpak.sh             # local dev: app module = working tree
#   scripts/build-flatpak.sh --release   # exact Flathub manifest (needs the
#                                        # git tag referenced in the manifest)
#
# Output: dist/BedrockOnLinux-<ver>-x86_64.flatpak
# Needs flatpak-builder + network (freedesktop runtime/SDK + bundled sources).
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VER="$(grep -m1 '^VERSION = ' "$SRC/bedrock-on-linux" | cut -d'"' -f2)"
APPID="io.github.wyze3306.BedrockOnLinux"
MANIFEST="$SRC/flatpak/$APPID.yml"
# The dev manifest lives in the same dir so ../ source paths resolve.
DEV_MANIFEST="$SRC/flatpak/.$APPID.resolved.yml"
OUT="$SRC/dist"
WORK="$OUT/flatpak-build"

if ! command -v flatpak-builder >/dev/null; then
  echo "– Flatpak skipped (flatpak-builder absent)."
  echo "  Debian/Ubuntu: sudo apt install flatpak-builder"
  echo "  Fedora:        sudo dnf install flatpak-builder"
  echo "  Arch:          sudo pacman -S flatpak-builder"
  exit 0
fi

mkdir -p "$WORK"

if ! flatpak remote-list 2>/dev/null | grep -q '^flathub'; then
  flatpak remote-add --user --if-not-exists flathub \
    https://flathub.org/repo/flathub.flatpakrepo || true
fi
flatpak install -y --user flathub \
  org.freedesktop.Platform//24.08 org.freedesktop.Sdk//24.08 2>/dev/null || \
  echo "  (runtime/SDK pre-install failed — flatpak-builder will fetch them)"

if [[ "${1:-}" == "--release" ]]; then
  BUILD_MANIFEST="$MANIFEST"
else
  # Dev build: swap the app module's pinned git source for the working tree,
  # laid out so the manifest's build-commands work unchanged.
  python3 -c 'import yaml' 2>/dev/null || {
    echo "needs PyYAML (e.g. sudo apt install python3-yaml)" >&2; exit 1; }
  python3 - "$MANIFEST" "$DEV_MANIFEST" <<'PY'
import sys, yaml
src, dst = sys.argv[1], sys.argv[2]
with open(src) as f:
    m = yaml.safe_load(f)
app = m["modules"][-1]
assert app["name"] == "bedrock-on-linux", "app module must be last"
app["sources"] = [
    {"type": "file", "path": "../bedrock-on-linux"},
    {"type": "file", "path": "../data/icon.png", "dest": "data"},
    {"type": "file", "path": "io.github.wyze3306.BedrockOnLinux.desktop",
     "dest": "flatpak"},
    {"type": "file", "path": "io.github.wyze3306.BedrockOnLinux.metainfo.xml",
     "dest": "flatpak"},
]
with open(dst, "w") as f:
    yaml.safe_dump(m, f, sort_keys=False)
print("dev manifest ->", dst)
PY
  BUILD_MANIFEST="$DEV_MANIFEST"
fi

flatpak-builder --user --force-clean --repo="$WORK/repo" \
  "$WORK/builddir" "$BUILD_MANIFEST"

BUNDLE="$OUT/BedrockOnLinux-${VER}-x86_64.flatpak"
flatpak build-bundle "$WORK/repo" "$BUNDLE" "$APPID"
ls "$OUT"/*.flatpak 2>/dev/null | grep -v "${VER}" | xargs -r rm -f

echo
echo "Built: $BUNDLE"
echo "Install: flatpak install --user $BUNDLE"
echo "Run:     flatpak run $APPID"
echo
echo "Lint (what Flathub CI runs):"
echo "  flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest $MANIFEST"