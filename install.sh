#!/usr/bin/env bash
# LocalFlow installer — clones (if needed), sets up a venv, installs deps, runs the app.
# Usage:
#   Remote one-liner:  curl -fsSL https://raw.githubusercontent.com/vmysla/LocalFlow/main/install.sh | bash
#   Local (in repo):   ./install.sh
set -euo pipefail

REPO_URL="https://github.com/vmysla/LocalFlow.git"
REPO_DIR="LocalFlow"

say() { printf "\033[1;36m==>\033[0m %s\n" "$*"; }
die() { printf "\033[1;31merror:\033[0m %s\n" "$*" >&2; exit 1; }

# --- prerequisites ---
command -v python3 >/dev/null || die "python3 not found. Install from https://www.python.org or with 'brew install python'."
command -v git     >/dev/null || die "git not found. Install Xcode CLT: 'xcode-select --install'."
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then
    say "ffmpeg missing — installing via Homebrew"
    brew install ffmpeg
  else
    die "ffmpeg not found. Install with 'brew install ffmpeg' (or see https://ffmpeg.org)."
  fi
fi

# --- clone if not already inside the repo ---
if [[ ! -f "ptt.py" || ! -f "requirements.txt" ]]; then
  if [[ -d "$REPO_DIR" ]]; then
    say "Found existing $REPO_DIR, pulling latest"
    git -C "$REPO_DIR" pull --ff-only
  else
    say "Cloning $REPO_URL"
    git clone "$REPO_URL" "$REPO_DIR"
  fi
  cd "$REPO_DIR"
fi

# --- venv + deps ---
if [[ ! -d ".venv" ]]; then
  say "Creating virtualenv in .venv"
  python3 -m venv .venv
fi

say "Installing Python dependencies (first run pulls PyTorch, ~100–200MB)"
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -r requirements.txt

# --- run ---
cat <<EOF

$(printf "\033[1;32m✓ Installed.\033[0m")

Launching LocalFlow now. On first use, macOS will prompt for:
  • Microphone access
  • Accessibility access (to listen for the hotkey and send ⌘V)
Grant both, then re-run if needed.

Default hotkey: hold Right Option (⌥), speak, release.
Quit with Ctrl+C in this terminal.

EOF

exec .venv/bin/python ptt.py
