# Product Requirements

## Overview

LocalFlow is a free, fully-local, open push-to-talk voice transcription tool for macOS. Holding the configured hotkey records microphone audio; releasing transcribes it via OpenAI Whisper running on-device and pastes the result into the focused application. No cloud, no account, no telemetry.

## Features

- **Push-to-talk transcription** — hold hotkey, speak, release; transcript is pasted at the cursor. _(Status: Implemented)_
  - Source: session 2026-04-20 · initial implementation
  - Artifacts: `ptt.py`

- **Clipboard preservation** — previous clipboard contents are restored after the transcription paste completes. _(Status: Implemented)_
  - Source: session 2026-04-20 · initial implementation
  - Artifacts: `ptt.py:_paste`

- **One-line installer** — remote `curl | bash` and local `./install.sh` paths; checks Python/git/ffmpeg, sets up venv, installs deps, launches app. _(Status: Implemented)_
  - Source: session 2026-04-20 · installer commit `aadd646`
  - Artifacts: `install.sh`

- **Permissions guidance** — README documents Microphone and Accessibility prompts on first launch and manual enablement fallback. _(Status: Implemented)_
  - Source: session 2026-04-20 · README polish commit `3c5b35b`
  - Artifacts: `README.md`

- **Launch article** — long-form narrative for Substack/Medium covering the 108-minute build, competitive pricing, and privacy contrast. _(Status: Implemented)_
  - Source: session 2026-05-14 · "write an article about how I created…"
  - Artifacts: `articles/wispr-flow-killer.md`

- **LinkedIn distribution config** — author/voice/audience/topics/hooks/CTAs/formatting/snippets configuration for the `write-linkedin-post` skill, scoped to Vlad Mysla's personal profile. _(Status: Implemented)_
  - Source: session 2026-05-14 · "Create me a linkedin post about this article."
  - Artifacts: `linkedin/config/company.md`, `audience.md`, `voice.md`, `topics.md`, `hooks.md`, `ctas.md`, `formatting.md`, `snippets.md`

- **LinkedIn post — Wispr moat (short, builder+founder audience)** — ≤800-char personal-profile post derived from `articles/wispr-flow-killer.md`; bold hook ("$144/year app in <2 hours"), single thesis line ("The moat was never the model"), dual CTA (article + repo links). _(Status: Draft)_
  - Source: session 2026-05-14 · "Create me a linkedin post about this article."
  - Artifacts: `linkedin/drafts/2026-05-14-1024-wispr-moat-152-lines.md`

## Configuration

- `MODEL_NAME` — `base.en` default; `tiny.en` (fastest) / `small.en` (more accurate) supported.
- `SAMPLE_RATE` — 16000 Hz mono, fixed to match Whisper expectations.
- `HOTKEY` — default `{keyboard.Key.alt_r}` (Right Option). Edit constant in `ptt.py`.
- `MIN_DURATION_SEC` — 0.3 s; clips shorter than this are ignored as accidental presses.

## Dependencies

- `openai-whisper` — on-device speech recognition (MIT licensed).
- `sounddevice` — microphone capture via PortAudio.
- `pynput` — global keyboard listener for hotkey detection.
- `numpy` — audio buffer concatenation.
- System: `python3` (3.9+), `git`, `ffmpeg` (auto-installed via Homebrew when missing).

## Architecture

Single-file Python app (`ptt.py`). Main thread runs a `pynput` keyboard listener; on hotkey press, an audio `InputStream` from `sounddevice` writes float32 chunks into an in-memory list under a lock. On release the buffer is concatenated and passed to a daemon thread that calls `MODEL.transcribe(...)`, then `pbcopy` + `osascript`-driven ⌘V to paste, then restores the previous clipboard contents on a delay. Whisper model is loaded once at startup and warmed up with silence so first real transcription isn't slow.

## Constraints

- macOS only (relies on `pbcopy`/`pbpaste` and `osascript` for paste).
- Requires Microphone and Accessibility permissions for the launching terminal/IDE.
- License: source-available for personal/educational/research use; commercial use requires written permission.
