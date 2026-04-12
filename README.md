# VS-DOS

A retro-inspired DOS simulator written in Python using `pygame`.

## What it is

`VS-DOS` is a nostalgic proof-of-concept DOS-style shell with a graphical text display, boot simulation, basic commands, and 16-color VGA-style rendering.

## Features

- Retro `C:\>` prompt experience
- A Award Modular BIOS styled launcher
- Boot POST simulation with BIOS/CPU/RAM/HDD output
- Basic command support:
  - `cls` — clear the screen
  - `ver` — show version information
  - `sysinfo` — display system info
  - `echo` — echo text back
  - `dir` — placeholder directory listing
  - `type` — placeholder file viewer
  - `colortest` — render a 16-color block test
  - `help` — list available commands
  - `exit` — quit the app
- Custom VGA-style color palette and DOS font rendering

## Files

- `main.py` — main application loop, input handling, command processing, and rendering
- `bios.py` — handles the POST screen for `main.py`
- `gui_colorful_test.py` — a Windows 3.1-styled GUI test
- `launcher.py` — a launcher for both main application and GUI test
- `fonts/Px437_IBM_VGA_8x16.ttf` — IBM VGA-style font used for rendering text
- `epa.png` — Energy Star logo for BIOS

## Requirements

- Python 3.x
- `pygame` (or `pygame-ce` for Python 3.14.x)

## Installation

1. Install Python 3 if needed.
2. If you are on Python 3.14.x, install `pygame-ce` instead of `pygame`:

```bash
python -m pip install pygame-ce
```

3. Otherwise, install `pygame`:

```bash
python -m pip install pygame
```

## Running

From the project folder:

```bash
python launcher.py
```

## Notes

- If the font file is missing, the app falls back to the system monospace font. (it'll usually don't happen)

## Thanks

Thanks int10h.org for fonts!

## License

MIT License
