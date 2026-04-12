import pygame
import sys
import time
import os
from bios import get_sys_info
from main import render_lines
import constants

FONT_PATH = constants.FONT_PATH
FONT_SIZE = constants.FONT_SIZE

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Award Modular BIOS v6.00PG Boot Menu")

try:
    dos_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except:
    print("Font file not found, using default.")
    dos_font = pygame.font.SysFont("monospace", FONT_SIZE)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    eslogo = pygame.image.load("fonts/epa.png").convert_alpha()
    eslogo = pygame.transform.scale(eslogo, (150, 100))
    logo_rect = eslogo.get_rect(topright=(screen.get_width() - 10, 10))
    lines = [
        f"{get_sys_info()['BIOS']}, An Energy Star Ally",
        get_sys_info()["BIOS2"],
        "",
        "GREEN AGP/PCI/ISA/AMR SYSTEM",
        "",
        'COL_SHOW:white;"BOOT MENU"',
        "",
        f'COL_SHOW:white;"1. " light_gray;"Disk C: ({get_sys_info()["OS"]}) [BOOT]"',
        'COL_SHOW:white;"2. " light_gray;"Disk D: (GUI Color Test)"',
        'COL_SHOW:white;"3. " light_gray;"Enter Setup"',
        'COL_SHOW:white;"4. " light_gray;"Shutdown"'
    ]
    render_lines(lines)
    screen.blit(eslogo, logo_rect)
    pygame.display.flip()
if __name__ == "__main__":
    main()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Boot VS-DOS
                    import main
                    main.main()
                elif event.key == pygame.K_2:
                    # Launch GUI Test
                    import gui_colorful_test
                    gui_colorful_test.main()
                elif event.key == pygame.K_3:
                    # Enter Setup
                    import bios
                    bios.bios_setup(screen, render_lines)
                elif event.key == pygame.K_4:
                    # Shutdown
                    pygame.quit()
                    sys.exit()