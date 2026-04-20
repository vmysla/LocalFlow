#!/usr/bin/env python3
"""Push-to-talk Whisper transcription.

Hold the hotkey, speak, release. Transcription is pasted into the focused element.
"""
import subprocess
import sys
import threading
import time

import numpy as np
import sounddevice as sd
import whisper
from pynput import keyboard

MODEL_NAME = "base.en"
SAMPLE_RATE = 16000
HOTKEY = {keyboard.Key.alt_r}
MIN_DURATION_SEC = 0.3

_state = {
    "keys": set(),
    "recording": False,
    "stream": None,
    "chunks": [],
    "start_time": 0.0,
}
_lock = threading.Lock()
_kbd = keyboard.Controller()


def canonicalize(key):
    """Normalize modifier keys. Left/right Option are kept distinct so each
    can be used as an independent hotkey; other modifiers are merged."""
    if key in (keyboard.Key.cmd_l, keyboard.Key.cmd_r):
        return keyboard.Key.cmd
    if key in (keyboard.Key.shift_l, keyboard.Key.shift_r):
        return keyboard.Key.shift
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        return keyboard.Key.ctrl
    return key


def _audio_callback(indata, frames, time_info, status):
    if status:
        print(f"audio status: {status}", file=sys.stderr)
    if _state["recording"]:
        _state["chunks"].append(indata.copy())


def start_recording():
    with _lock:
        if _state["recording"]:
            return
        _state["chunks"] = []
        _state["recording"] = True
        _state["start_time"] = time.time()
        _state["stream"] = sd.InputStream(
            channels=1, samplerate=SAMPLE_RATE, dtype="float32",
            callback=_audio_callback,
        )
        _state["stream"].start()
    print("● recording…", flush=True)


def stop_recording():
    with _lock:
        if not _state["recording"]:
            return
        _state["recording"] = False
        stream = _state["stream"]
        _state["stream"] = None
        chunks = _state["chunks"]
        duration = time.time() - _state["start_time"]
    if stream is not None:
        stream.stop()
        stream.close()
    print(f"■ stopped ({duration:.2f}s), transcribing…", flush=True)
    if duration < MIN_DURATION_SEC or not chunks:
        print("(too short, ignored)", flush=True)
        return
    audio = np.concatenate(chunks, axis=0).flatten().astype(np.float32)
    threading.Thread(target=_transcribe_and_paste, args=(audio,), daemon=True).start()


def _transcribe_and_paste(audio):
    t0 = time.time()
    result = MODEL.transcribe(audio, fp16=False, language="en")
    text = result["text"].strip()
    elapsed = time.time() - t0
    if not text:
        print(f"(no speech detected, {elapsed:.2f}s)", flush=True)
        return
    print(f"→ {text}  [{elapsed:.2f}s]", flush=True)
    _paste(text)


def _paste(text):
    # Preserve existing clipboard, paste transcription, restore.
    try:
        prev = subprocess.run(["pbpaste"], capture_output=True).stdout
    except Exception:
        prev = None
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
    # Let the OS register the clipboard update before sending Cmd+V.
    time.sleep(0.1)
    result = subprocess.run(
        ["osascript", "-e",
         'tell application "System Events" to keystroke "v" using command down'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"paste failed: {result.stderr.strip()}", flush=True)
        print("(text is on the clipboard; press ⌘V manually)", flush=True)
    if prev is not None:
        # Restore after paste is consumed by the focused app.
        def restore():
            time.sleep(0.6)
            subprocess.run(["pbcopy"], input=prev, check=False)
        threading.Thread(target=restore, daemon=True).start()


def on_press(key):
    k = canonicalize(key)
    _state["keys"].add(k)
    if HOTKEY.issubset(_state["keys"]) and not _state["recording"]:
        start_recording()


def on_release(key):
    k = canonicalize(key)
    was_active = HOTKEY.issubset(_state["keys"])
    _state["keys"].discard(k)
    if was_active and k in HOTKEY and _state["recording"]:
        stop_recording()


def main():
    global MODEL
    print(f"Loading Whisper model '{MODEL_NAME}'…", flush=True)
    MODEL = whisper.load_model(MODEL_NAME)
    # Warm up with silence so the first real transcription isn't slow.
    MODEL.transcribe(np.zeros(SAMPLE_RATE, dtype=np.float32), fp16=False, language="en")
    keys_desc = " + ".join(str(k).replace("Key.", "") for k in HOTKEY)
    print(f"Ready. Hold {keys_desc} to record; release to transcribe.", flush=True)
    print("Press Ctrl+C in this terminal to quit.", flush=True)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
