import pygame
import sys
import os
import time
from bios import get_sys_info

FONT_PATH = os.path.join("fonts", "Px437_IBM_VGA_8x16.ttf")
FONT_SIZE = 16

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("VS-DOS Beta 2 Prompt")

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

def colors2():
    return colors

def get_color_names():
    return list(colors.keys())

try:
    dos_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except:
    print("Font file not found, using default.")
    dos_font = pygame.font.SysFont("monospace", FONT_SIZE)

def render_lines(lines):
    screen.fill(colors["black"])
    for i, line in enumerate(lines):
        # Special check: is this a color test line?
        # We look for a special prefix like "COL_SHOW:"
        if line.startswith("COL_SHOW:"):
            color_name = line.split(":")[1]
            actual_color = colors.get(color_name, colors["white"])
            
            # Draw the label
            label = dos_font.render(f"{color_name.upper():<10}", True, colors["white"])
            screen.blit(label, (10, 10 + (i * FONT_SIZE)))
            
            # Draw the color block [████████]
            pygame.draw.rect(screen, actual_color, (120, 10 + (i * FONT_SIZE), 100, FONT_SIZE - 2))
        else:
            # Normal text rendering
            text_surface = dos_font.render(line, True, colors["white"])
            screen.blit(text_surface, (10, 10 + (i * FONT_SIZE)))
    
    pygame.display.flip()

def run_post():
    info = get_sys_info()
    lines = [
        info["BIOS"],
        f"CPU: {info['CPU']}",
        "Memory Test: 0 KB",
    ]
    
    # Simulate RAM counting
    for ram in range(0, info["RAM"] + 1, 4096):
        lines[2] = f"Memory Test: {ram} KB OK"
        render_lines(lines)
        time.sleep(0.05)
    
    lines.append(f"Fixed Disk 0: {info['HDD']} MB")
    lines.append("")
    lines.append("Starting VS-DOS...")
    render_lines(lines)
    time.sleep(1)
    return ["VS-DOS Beta 1", "MIT License, GitDanyaUser", ""]

def dirlist():
    #TODO: Well, implement later
    return "This feauture is not implemented yet, come back in a final release!"

def catfile(filename):
    #TODO: Same as above, implement later
    return "This feauture is not implemented yet, come back in a final release!"

def colortest():
    color_names = get_color_names()
    lines = []
    for color in color_names:
        lines.append(f"COL_SHOW:{color}")
    return lines

def main():
    display_history = run_post()
    current_input = "C:\\> "
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Process command
                    cmd = current_input.replace("C:\\> ", "").strip().lower()
                    display_history.append(current_input)
                    
                    if cmd == "cls":
                        display_history = []
                    elif cmd == "ver":
                        display_history.append("VS-DOS Beta 1")
                    elif cmd == "sysinfo":
                        info = get_sys_info()
                        display_history.append(f"BIOS: {info['BIOS']}")
                        display_history.append(f"CPU: {info['CPU']}")
                        display_history.append(f"RAM: {info['RAM']} KB")
                        display_history.append(f"HDD: {info['HDD']} MB")
                    elif cmd.startswith("echo "):
                        display_history.append(cmd[5:])
                    elif cmd.startswith("dir"):
                        display_history.append(dirlist())
                    elif cmd.startswith("type "):
                        filename = cmd[5:].strip()
                        display_history.append(catfile(filename))
                    elif cmd == "colortest":
                        display_history.append("Be sure your moinitor supports 16 colors to see the test properly!")
                        render_lines(display_history)
                        time.sleep(3)
                        display_history = []
                        display_history.append("== IBM VGA 16 Color Test ==")
                        display_history.extend(colortest())
                        display_history.append("===========================")
                    elif cmd == "help":
                        display_history.append("Available commands: cls, ver, sysinfo, echo, dir, type, colortest, help, exit")
                    elif cmd == "exit":
                        pygame.quit()
                        sys.exit()
                    elif cmd != "":
                        display_history.append(f"Bad command or file name: {cmd}")
                    
                    current_input = "C:\\> "
                
                elif event.key == pygame.K_BACKSPACE:
                    if len(current_input) > 5: # Don't delete "C:\> "
                        current_input = current_input[:-1]
                else:
                    current_input += event.unicode

        # Keep only the last 25 lines to fit the screen
        blink = "_" if int(time.time() * 2) % 2 == 0 else " "
        visible_lines = display_history[-25:] + [current_input + blink]
        render_lines(visible_lines)

if __name__ == "__main__":
    main()