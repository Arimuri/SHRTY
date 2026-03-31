# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SHRTY is a standalone visual synthesizer for macOS (Windows porting in progress), based on [EYESY_OS](https://github.com/critterandguitari/EYESY_OS) by Critter & Guitari. It captures real-time audio and MIDI input and renders responsive visuals using 150+ dynamically-loaded Python/Pygame modes.

## Running the Application

```bash
# macOS / Linux
./run.sh
```

`run.sh` automatically creates a Python 3.9+ venv, installs `requirements.txt`, and launches `shrty.py`. There is no formal test suite; the app includes a menu-accessible "Test Screen" for hardware testing.

For Windows, `run.bat` or `run.ps1` does not yet exist — see `TODO_windows.md` for the full porting checklist.

## Architecture

```
shrty.py          # Main event loop, pygame setup, key/MIDI dispatch, recording
eyesy.py          # Central state machine (Eyesy class): mode loading, scenes, config, knobs
sound_mac.py      # Multiprocess audio capture via sounddevice + numpy
midi_mac.py       # MIDI input via mido + python-rtmidi
osd.py            # On-screen display: knobs, VU meters, menus
config.py         # JSON config load/save
file_operations.py# File/folder operations (zip, copy, delete)
screen_*.py       # Menu screen implementations (Main, MIDI, Palette, etc.)
widget_*.py       # Reusable UI components (menu, keyboard, dialog, etc.)
data/Modes/       # 150+ visual mode directories, each with main.py
```

### Mode System

Each mode lives in `data/Modes/<ModeName>/main.py` and must define:
```python
def setup(screen, eyesy): ...
def draw(screen, eyesy): ...
```

Modes are loaded at runtime via `importlib.util`. They access audio buffers, MIDI state, and knob values through the `eyesy` object. Mode naming convention: `[Creator] - [Type] - [Name]`.

### Audio Pipeline

`sound_mac.py` runs audio capture in a separate `multiprocessing.Process` to avoid blocking the 30fps render loop, writing to shared memory buffers that `eyesy.py` reads each frame.

### Dual Mode (SHRTY-specific)

TAB toggles a second mode running simultaneously, blended with the primary using Add / Multiply / Crossfade blend modes (C key cycles, V/B adjust mix ratio).

## Windows Porting Status

All known issues are tracked in `TODO_windows.md`. Key areas:

1. **Startup script** — Need `run.bat`/`run.ps1` (`source venv/bin/activate` → `venv\Scripts\activate.bat`)
2. **Data paths** — `eyesy.py` lines 23–26 hardcode `/sdcard/...`; need `platform.system()` branching to use `os.path.join(os.path.dirname(__file__), "data", ...)`
3. **`os.system('mkdir ...')`** — `eyesy.py` lines 282, 594; replace with `os.makedirs(..., exist_ok=True)`
4. **Font paths** — Many files use relative `"font.ttf"`; should use `os.path.join(SHRTY_DIR, "font.ttf")` like `shrty.py` already does. Affected: `osd.py`, `screen.py`, `screen_flash_drive.py`, `widget_*.py`
5. **`file_operations.py`** — `BASE_DIR = "/"` is meaningless on Windows; `os.system("unzip")`/`os.system("zip")` must be replaced with Python's `zipfile` module; all path joins need `os.path.join()`
6. **MIDI filtering** — `midi_mac.py:70` filters `"Midi Through"` (Linux-only port name); Windows needs platform-specific port exclusion patterns

System-management screens (WiFi, Video Settings, Hardware Test) fail gracefully on non-Linux — the broad `except Exception` handler in `shrty.py:537` catches Linux-only command errors, matching macOS behavior. No fix needed.
