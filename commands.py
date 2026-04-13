import sys
import pygame
import datetime
from bios import get_sys_info
import time
import constants
import os
import gui_stuff

colors = constants.colors
SYSTEM_FILES = constants.SYSTEM_FILES
FONT_PATH = constants.FONT_PATH
FONT_SIZE = constants.FONT_SIZE

try:
    win_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except:
    win_font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)

def timetell():
    time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    return time

def gputest(render_lines, colors: dict):
    lines = [
        f"GPU: {get_sys_info()["GPU"]}",
        f"VGA BIOS: {get_sys_info()["VGABIOS"]}",
        "",
        "",
        "",
        "<<< GPU VGA Test >>>",
    ]
    lines2 = [
        "<<<==============>>>",
        "<<< Colored text test >>>",
        'COL_SHOW:red;"Red " green;"Green " blue;"Blue"',
        "<<<===================>>>",
        "Test completed!",
        "Press Enter to return to shell."
    ]
    render_lines(lines)
    color_names = list(colors.keys())
    for color in color_names:
        lines.append(f'COL_SHOW:{color};"████████████████"')
        render_lines(lines)
        time.sleep(0.02)
    lines.extend(lines2)
    render_lines(lines)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def editor(render_lines, screen, dos_font, colors, current_phys_path, args):
    if not args: return "Usage: EDIT [filename]"
    
    filename = args[0].lower()
    file_path = os.path.join(current_phys_path, filename)
    boot_lines = [
        "DOS Edit v1.0",
        "DEBUG: Disabled",
        "DRIVE: C",
        f"SYSTEM: {get_sys_info()["OS"]}"
    ]
    render_lines(boot_lines, colors["blue"], colors["white"])
    time.sleep(1)
    content = ""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()

    # --- GUI EDITOR INTERNAL LOOP ---
    lines = content.split('\n') if content else [""]
    cursor_x, cursor_y = 0, 0
    char_w, char_h = dos_font.size("A")
    editing = True
    
    while editing:
        screen.fill((30, 30, 30)) # Dark third-party background
        
        # Header & Footer bars
        pygame.draw.rect(screen, colors["light_gray"], (0, 0, 640, char_h + 4))
        pygame.draw.rect(screen, colors["light_gray"], (0, 480 - (char_h + 4), 640, char_h + 4))
        
        # Text
        screen.blit(dos_font.render(f" EDITING: {filename.upper()}", True, (0,0,0)), (5, 2))
        screen.blit(dos_font.render(" [F2] Save & Exit   [ESC] Abandon", True, (0,0,0)), (5, 478 - char_h))

        for i, text in enumerate(lines):
            screen.blit(dos_font.render(text, True, colors["white"]), (10, (char_h + 10) + (i * char_h)))

        # Cursor
        if int(time.time() * 2) % 2 == 0:
            pygame.draw.rect(screen, colors["white"], (10 + (cursor_x * char_w), (char_h + 10) + (cursor_y * char_h), char_w, char_h))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2: # SAVE
                    with open(file_path, "w") as f:
                        f.write("\n".join(lines))
                    return f"File {filename} saved successfully."
                
                if event.key == pygame.K_ESCAPE: # CANCEL
                    return "Edit aborted."

                # Basic Movement & Typing
                if event.key == pygame.K_UP: cursor_y = max(0, cursor_y - 1); cursor_x = min(cursor_x, len(lines[cursor_y]))
                elif event.key == pygame.K_DOWN: cursor_y = min(len(lines)-1, cursor_y + 1); cursor_x = min(cursor_x, len(lines[cursor_y]))
                elif event.key == pygame.K_LEFT: cursor_x = max(0, cursor_x - 1)
                elif event.key == pygame.K_RIGHT: cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
                elif event.key == pygame.K_RETURN:
                    lines.insert(cursor_y + 1, lines[cursor_y][cursor_x:])
                    lines[cursor_y] = lines[cursor_y][:cursor_x]
                    cursor_y += 1; cursor_x = 0
                elif event.key == pygame.K_BACKSPACE:
                    if cursor_x > 0:
                        lines[cursor_y] = lines[cursor_y][:cursor_x-1] + lines[cursor_y][cursor_x:]
                        cursor_x -= 1
                    elif cursor_y > 0:
                        cursor_x = len(lines[cursor_y-1])
                        lines[cursor_y-1] += lines.pop(cursor_y); cursor_y -= 1
                elif event.unicode.isprintable() and event.unicode != "":
                    lines[cursor_y] = lines[cursor_y][:cursor_x] + event.unicode + lines[cursor_y][cursor_x:]
                    cursor_x += 1
def delete(current_phys_path, args):
    if not args:
        return "Required parameter missing"

    filename = args[0].lower()
    
    # 1. Protection Check
    if filename in SYSTEM_FILES:
        return "Access denied - System file protected."

    # 2. Path Resolution
    file_path = os.path.join(current_phys_path, filename)

    # 3. Execution
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            return "Target is a directory."
        
        try:
            os.remove(file_path)
            return f"File {filename.upper()} deleted."
        except Exception as e:
            return f"Disk Error: {e}"
    else:
        return "File not found."

def mgmt(screen, colors):
    screen.fill(colors["blue"])
    gui_stuff.draw_window(win_font, screen, "Stat Manager", 0, 0, 640, 480, close=False)
    msg = win_font.render(f"RAM: {get_sys_info()["RAM"] / 1000}KB", True, colors["black"])
    screen.blit(msg, (30, 30))
    msg2 = win_font.render(f"HDD: {get_sys_info()["HDD"]}MB", True, colors["black"])
    screen.blit(msg2, (30, 50))
    msg3 = win_font.render(f"OS: {get_sys_info()["OS"]}", True, colors["black"])
    screen.blit(msg3, (30, 70))
    
    msgexit = win_font.render(f"Press Enter to exit", True, colors["black"])
    screen.blit(msgexit, (30, 450))

    # Render everything
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False