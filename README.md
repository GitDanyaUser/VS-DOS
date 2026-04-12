# VS-DOS

A retro-inspired DOS simulator written in Python using `pygame`.

## What it is

`VS-DOS` is a nostalgic proof-of-concept DOS-style shell with a graphical text display, boot simulation, basic commands, and 16-color VGA-style rendering.

## Screenshots

<img width="642" height="512" alt="Записати1" src="https://github.com/user-attachments/assets/86fde9b3-5f2c-4ec0-83c2-c040631104b2" />

<img width="638" height="508" alt="Записати" src="https://github.com/user-attachments/assets/3e3806b4-9542-4905-b23f-ed49b6793553" />

<img width="633" height="514" alt="Записати2" src="https://github.com/user-attachments/assets/9ab42bc6-dc25-4527-a4dc-c84873cf9d7d" />

<img width="642" height="512" alt="Записати3" src="https://github.com/user-attachments/assets/e81ed96c-0e0c-42ce-a568-8e4fb0f92ead" />

## Features

- Retro `C:\>` prompt experience
- A Award Modular BIOS styled launcher
- Boot POST simulation with BIOS/CPU/RAM/HDD output
- Basic command support:
  - `cls` — clear the screen
  - `ver` — show version information
  - `sysinfo` — display system info
  - `echo` — echo text back
  - `dir` — directory listing
  - `type` — file viewer
  - `colortest` — render a 16-color block test
  - `edit` — placeholder for editor
  - `help` — list available commands
  - `exit` — quit the app
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
- It's still in beta! Expect a lot of issues.

## Thanks

Thanks int10h.org for fonts!

## License

MIT License
