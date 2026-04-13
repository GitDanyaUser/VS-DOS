import os

FONT_PATH = os.path.join("fonts", "Px437_IBM_VGA_8x16.ttf")
FONT_SIZE = 16
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_NAME = "storage"
STORAGE_PATH = os.path.join(BASE_DIR, STORAGE_NAME)
SYSTEM_FILES = ["autoexec.bat", "config.sys", "command.com", "io.sys", "msdos.sys"]

colors = {
    "black": (0, 0, 0),
    "blue": (0, 0, 170),
    "green": (0, 170, 0),
    "cyan": (0, 170, 170),
    "red": (170, 0, 0),
    "magenta": (170, 0, 170),
    "brown": (170, 85, 0),
    "light_gray": (170, 170, 170),
    "dark_gray": (85, 85, 85),
    "light_blue": (85, 85, 255),
    "light_green": (85, 255, 85),
    "light_cyan": (85, 255, 255),
    "light_red": (255, 85, 85),
    "light_magenta": (255, 85, 255),
    "yellow": (255, 255, 85),
    "white": (255, 255, 255)
}

colors256 = {
    #TODO: Add 256 colors and maybe switch fully to using this in the future
}

def get_color_names():
    return list(colors.keys())