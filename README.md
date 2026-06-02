# VS-DOS

A retro-inspired DOS simulator written in Python using `pygame`.

## What it is

`VS-DOS` is a nostalgic DOS-style shell with a graphical text display, boot simulation, basic commands, and 16-color VGA-style rendering.

## Screenshots

<img width="642" height="512" alt="Записати" src="https://github.com/user-attachments/assets/a4730cde-a7f1-455f-be5d-03195c81f984" />

<img width="642" height="512" alt="Записати1" src="https://github.com/user-attachments/assets/cd95fa97-1d65-452e-b0a6-02f0fe9b950b" />

<img width="642" height="512" alt="Записати2" src="https://github.com/user-attachments/assets/eccd7f3a-414e-4977-a621-b6e6504227c6" />

<img width="642" height="512" alt="Записати3" src="https://github.com/user-attachments/assets/8736e02e-ce70-41ed-ad6e-dd7057540fc8" />

<img width="642" height="512" alt="Записати4" src="https://github.com/user-attachments/assets/67613189-934b-4cf6-a808-707ceadc7228" />

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

GPL-3.0 License
