# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SHRTY is a standalone visual synthesizer for macOS and Windows, based on [EYESY_OS](https://github.com/critterandguitari/EYESY_OS) by Critter & Guitari. It captures real-time audio and MIDI input and renders responsive visuals using 150+ dynamically-loaded Python/Pygame modes.

## Running the Application

```bash
# macOS / Linux
./run.sh

# Windows
run.bat
```

Both scripts automatically create a Python 3.9+ venv, install `requirements.txt`, and launch `shrty.py`. There is no formal test suite; the app includes a menu-accessible "Test Screen" for hardware testing.

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

Key `eyesy` properties available in modes:
- `eyesy.knob1`–`eyesy.knob5`: `0.0`–`1.0`
- `eyesy.audio_in[0:99]`: audio buffer (`-32768`–`32767`)
- `eyesy.audio_peak`: peak value
- `eyesy.color_picker(t)` / `eyesy.color_picker_bg(t)`: palette color at `t` (`0.0`–`1.0`)
- `eyesy.trig`: trigger boolean
- `eyesy.midi_notes[0:127]`: MIDI note states

### Audio Pipeline

`sound_mac.py` runs audio capture in a separate `multiprocessing.Process` to avoid blocking the 30fps render loop, writing to shared memory buffers that `eyesy.py` reads each frame.

### Dual Mode (SHRTY-specific)

TAB toggles a second mode running simultaneously, blended with the primary using Add / Multiply / Crossfade blend modes (C key cycles, V/B adjust mix ratio).

### Platform Handling

`eyesy.py` uses `platform.system() == "Windows"` to branch data paths (`data/` relative to the script vs. `/sdcard` on Linux). System-management screens (WiFi, Video Settings, Hardware Test) fail gracefully on non-Linux via broad `except Exception` handling in `shrty.py`.

Font paths use `os.path.join(SHRTY_DIR, "font.ttf")` for cross-platform compatibility. `file_operations.py` uses Python's `zipfile` module (not shell `zip`/`unzip`). MIDI port filtering in `midi_mac.py` is platform-aware.
