# VS-DOS

A retro-inspired DOS simulator written in Python using `pygame`.

## What it is

`VS-DOS` is a nostalgic proof-of-concept DOS-style shell with a graphical text display, boot simulation, basic commands, and 16-color VGA-style rendering.

## Screenshots



## Features

- Retro `C:\>` prompt experience
- A Award Modular BIOS styled launcher
- Boot POST simulation with BIOS/CPU/RAM/HDD output
- VGA-style color palette and DOS font rendering

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
- It will not format your actual drive! This is just simulation

## Thanks

Thanks int10h.org for fonts!

## License

MIT License
