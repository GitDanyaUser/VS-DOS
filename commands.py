import sys
import pygame
import datetime
from bios import get_sys_info, bios_post
import time
import constants
import os
import gui_stuff
import vfsinit
from utils import sleep

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
        sleep(0.02)
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

def editor(screen, dos_font, colors, current_phys_path, args):
    if not args: return "Usage: EDIT [filename]"
    
    filename = args[0].lower()
    file_path = os.path.join(current_phys_path, filename)

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

def stat(screen, colors):
    screen.fill(colors["blue"])
    gui_stuff.draw_window(screen, "Stat Manager", 0, 0, 640, 480, close=False)
    msg = win_font.render(f"RAM: {get_sys_info()["RAM"] // 1024}KB", True, colors["black"])
    screen.blit(msg, (30, 30))
    msg2 = win_font.render(f"CPU: {get_sys_info()["CPU"]}", True, colors["black"])
    screen.blit(msg2, (30, 50))
    msg3 = win_font.render(f"OS: {get_sys_info()["OS"]}", True, colors["black"])
    screen.blit(msg3, (30, 70))
    msg4 = win_font.render(f"HDD Total: {get_sys_info()["HDD"]}MB", True, colors["black"])
    screen.blit(msg4, (30, 90))
    msg5 = win_font.render(f"HDD Free: {vfsinit.get_vfs_metadata()["free"] // (1024*1024)}MB", True, colors["black"])
    screen.blit(msg5, (30, 110))

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

def vsdos_setup(render_lines, colors, skip=False):
    def lines_right(lines, spaces=5):
        return [" " * spaces + line for line in lines]

    def add_lines(lines):
        return top_lines + lines_right(lines)
    
    def wait_for_input(current_screen, target_key=None):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Check for KEYDOWN first to avoid AttributeErrors
                if event.type == pygame.KEYDOWN:
                    # ESCAPE HANDLER
                    if event.key == pygame.K_ESCAPE:
                        ask = [
                            "Are you sure to cancel the installation process?",
                            "",
                            "Press Y to exit the wizard",
                            "Press N to return"
                        ]
                        render_lines(ask, colors["blue"], colors["white"])
                        
                        waiting2 = True
                        while waiting2:
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if ev.type == pygame.KEYDOWN:
                                    if ev.key == pygame.K_y:
                                        pygame.quit()
                                        sys.exit()
                                    elif ev.key == pygame.K_n:
                                        render_lines(top_lines + lines_right(current_screen), colors["blue"], colors["white"])
                                        waiting2 = False
                    
                    # Target key logic (only runs if KEYDOWN)
                    if target_key is None:
                        if event.key == pygame.K_RETURN:
                            waiting = False
                    elif event.key == target_key:
                        waiting = False

    if skip:
        return
    top_lines = [
        "=====================",
        " VS-DOS Installation",
        "=====================",
    ]
    install_lines = [
        "",
        "",
        "Welcome to the VS-DOS Installation Wizard!",
        "This wizard will guide you through the installation of VS-DOS",
        "",
        "VS-DOS allows you to manage disk files, also VS-DOS supports VGA",
        "",
        "Press Enter to begin the installation process",
        "",
        "Press ESC to exit the installer"
    ]
    install_lines2 = [
        "",
        "",
        "This will format the drive, are you sure to continue?",
        "",
        "Press C to format the drive",
        "",
        "Press ESC to exit the installer"
    ]
    install_lines3 = [
        "",
        "",
        "Thanks for installing VS-DOS!",
        "To see all of the avaiable commands, type 'help'",
        "",
        "Press Enter to exit the installer"
    ]
    wait_lines = [
        "",
        "",
        "Please wait while installation wizard formats the drive..."
    ]
    files = [
        "C:\\COMMAND.COM",
        "C:\\DOS\\IO.SYS",
        "C:\\DOS\\VSDOS.SYS",
        "C:\\DOS\\MOUSE.SYS",
        "C:\\DOS\\EDIT.COM",
        "C:\\CONFIG.SYS",
        "C:\\AUTOEXEC.BAT",
        "C:\\README.TXT"
    ]
    render_lines(add_lines(install_lines), colors["blue"], colors["white"])
    wait_for_input(install_lines)
    render_lines(add_lines(install_lines2), colors["blue"], colors["white"])
    wait_for_input(install_lines2, target_key=pygame.K_c)
    render_lines(add_lines(wait_lines), colors["blue"], colors["white"])
    sleep(6)
    for i, fname in enumerate(files):
        wait_lines2 = [
            "",
            "",
            f"Copying files...",
            f"Target: {fname}",
            "",
            "Please wait as setup copying files"
        ]
        render_lines(add_lines(wait_lines2), colors["blue"], colors["white"])
        sleep(1.5)
    render_lines(add_lines(install_lines3), colors["blue"], colors["white"])
    wait_for_input(install_lines3)
    with open(os.path.join(constants.STORAGE_PATH, "install.txt"), "w") as f:
        f.write("Delete me if you want to see installer again")

def vsshell(screen, colors):
    screen.fill(colors["light_gray"])
    gui_stuff.draw_window2(screen, "VS-DOS Graphical Window Manager", 0, 0, 640, 480, close=False)

    msg = win_font.render("This feature is not implemented yet, come back in v1.0.0!", True, colors["black"])
    screen.blit(msg, (10, 30))
    msg2 = win_font.render("Press Enter to return to shell", True, colors["black"])
    screen.blit(msg2, (10, 440))

    msg3 = win_font.render("For now, look at this cool elements!", True, colors["black"])
    screen.blit(msg3, (10, 60))

    gui_stuff.draw_button(screen, "Button 1", 10, 100, 120, 30)

    gui_stuff.draw_fixed_list(screen, ["Item 1", "Item 2", "Item 3", "Item 4"], 10, 150, 200, 100)
    
    gui_stuff.draw_window2(screen, "Nested Window", 300, 100, 200, 150)

    gui_stuff.draw_block(screen, 300, 300, 100, 100, colors["light_red"])
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

def diag(screen, render_lines, colors):
    bios_post(screen, render_lines)

    top_lines = [
        "===============================",
        " VS-DOS Diagnostic Environment",
        "==============================="
    ]

    def lines_right(lines, spaces=5):
        return [" " * spaces + line for line in lines]

    def add_lines(lines):
        return top_lines + lines_right(lines)
    
    def wait_for_input(target_keys=[pygame.K_RETURN, pygame.K_ESCAPE]):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in target_keys:
                        return event.key
                        waiting = False
        
    diag_lines = [
        "",
        "",
        "Welcome to the VS-DOS Diagnostic Environment!",
        "Use this environment to test your hardware and troubleshoot issues.",
        "",
        "Press 1 to see GPU information",
        "Press 2 to see common hardware information",
        "Press ESC to return to the shell"
    ]
    render_lines(add_lines(diag_lines), colors["blue"], colors["white"])
    key = wait_for_input(target_keys=[pygame.K_1, pygame.K_2, pygame.K_ESCAPE])
    if key == pygame.K_ESCAPE:
        pass
    elif key == pygame.K_1:
        gpu_lines = [
            "",
            "",
            f"GPU: {get_sys_info()['GPU']}",
            f"VGA BIOS: {get_sys_info()['VGABIOS']}",
            "",
            "Supported Resolutions:",
            "- 640x480 @ 16 colors",
            "- 320x200 @ 16 colors",
            "- 80x25 text mode",
            "",
            "Driver: vgadrvr.sys",
            "Driver: Generic VGA Driver (inside vsdos.sys)",
            "",
            "No hardware issues detected.",
            "",
            "Press Enter to return to the shell"
        ]
        render_lines(add_lines(gpu_lines), colors["blue"], colors["white"])
        wait_for_input()
    elif key == pygame.K_2:
        sys_lines = [
            "",
            "",
            f"CPU: {get_sys_info()['CPU']}",
            f"RAM: {get_sys_info()['RAM'] // 1024}KB",
            f"HDD Total: {get_sys_info()['HDD']}MB",
            f"HDD Free: {vfsinit.get_vfs_metadata()['free'] // (1024*1024)}MB",
            "",
            "Press Enter to return to the shell"
        ]
        render_lines(add_lines(sys_lines), colors["blue"], colors["white"])
        wait_for_input()