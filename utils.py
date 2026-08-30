import pygame
import sys
import string
import os
import constants

colors = constants.colors

def sleep(seconds):
    end_time = pygame.time.get_ticks() + (seconds * 1000)
    while pygame.time.get_ticks() < end_time:
        pygame.event.pump()
        pygame.time.delay(10)

def bsod(render_lines, code="0x0000003b", code_desc="SYSTEM_SERVICE_EXCEPTION"):
    lines = [
        "A problem has been detected and VS-DOS has been shut down to prevent damage",
        "to your computer.",
        "If this is the first time you've seen this Stop error screen, restart your ",
        "computer.",
        "",
        "If this screen appears again, follow these steps:",
        "Check to make sure any new hardware or software is properly installed.",
        "",
        f"Technical information: {code} ({code_desc})"
    ]

    render_lines(lines, bg_color=colors["blue"], text_color=colors["white"])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def gen_rand_bytes(byte_size=1000):
    return os.urandom(byte_size)


def gen_rand_string(byte_size=1000):
    character_pool = string.ascii_letters + string.digits + string.punctuation
    pool_len = len(character_pool)
    
    random_source = os.urandom(byte_size)
    char_list = [character_pool[b % pool_len] for b in random_source]
    
    return ''.join(char_list)

def return_bytes_from_root(filepath):
    """
    Reads and returns the raw bytes of a file located in the project root directory.
    Example: data = return_from_root("fonts/epa.png")
    """
    target_path = os.path.abspath(os.path.join(constants.BASE_DIR, filepath))
    
    if os.path.exists(target_path) and os.path.isfile(target_path):
        try:
            with open(target_path, "rb") as f:
                return f.read()
        except Exception:
            return None
    return None