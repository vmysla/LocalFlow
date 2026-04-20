# LocalFlow

Free, fully-local, private and open source alternative to Wispr Flow / Superwhisper / Monologue / etc.

Push-to-talk voice transcription for macOS, powered by OpenAI Whisper running locally. Hold a hotkey, speak, release — the transcription is pasted into whatever window is focused. No cloud, no API keys, no data leaves your machine.

Repo: https://github.com/vmysla/LocalFlow

## Install & run

One-liner — clones the repo, sets up a venv, installs dependencies, and launches the app:

```bash
curl -fsSL https://raw.githubusercontent.com/vmysla/LocalFlow/main/install.sh | bash
```

Or, if you've already cloned the repo:

```bash
./install.sh
```

Requires Python 3.9+, git, and ffmpeg. The installer will use Homebrew to install ffmpeg if it's missing.

Subsequent runs (after install):

```bash
.venv/bin/python ptt.py
```

**Default hotkey:** hold **Right Option (⌥)**, speak, release. Transcription is pasted at the cursor.

To change the hotkey or Whisper model, edit the constants at the top of `ptt.py`:

- `HOTKEY` — e.g. `{keyboard.Key.f19}` for F19, or `{keyboard.Key.ctrl, keyboard.Key.alt}` for Ctrl+Option
- `MODEL_NAME` — `tiny.en` (fastest), `base.en` (default), `small.en` (more accurate)

## Permissions

macOS requires two permissions for the terminal app (or IDE) that launches the script. **The app asks for both on first use** via standard macOS prompts — just click "Open System Settings" and toggle them on. If the prompts don't appear or you need to enable them manually:

**System Settings → Privacy & Security:**

1. **Microphone** — to capture audio
2. **Accessibility** — to listen for the global hotkey and send ⌘V to paste

Add your terminal application (Terminal, iTerm, VS Code, Cursor, etc.) to **both** lists and toggle them on. After granting, fully quit (⌘Q) and relaunch the terminal, then re-run the script.

If paste fails with `osascript is not allowed to send keystrokes (1002)`, the transcription is still on your clipboard and you can press ⌘V manually. Grant Accessibility to your terminal to fix it.

## How it works

- Loads the Whisper model once at startup and warms it up with silence so the first transcription is fast.
- While the hotkey is held, mic audio streams into an in-memory buffer (16 kHz mono).
- On release, the buffer is transcribed directly (no temp files), copied to the clipboard, pasted with ⌘V, and your previous clipboard contents are restored.

## License

See [LICENSE.md](LICENSE.md).
