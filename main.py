import pygame
import sys
import os
import time
from bios import get_sys_info, bios_post
import constants
import re
import vfsinit
import commands
from utils import sleep

FONT_PATH = constants.FONT_PATH
FONT_SIZE = constants.FONT_SIZE

# --- INITIALIZATION ---
vfsinit.init_vfs()
current_path = []  # Empty list represents Root (C:\)

def get_real_current_path():
    """Helper to get the physical path for the current virtual directory."""
    # Joins 'storage/' with the folders in our current_path list
    return os.path.join(constants.STORAGE_PATH, *current_path)

pygame.init()
print("Pygame initiated")
# Initialize Pygame and the Mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Mixer initiated (2 channels)")

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("VS-DOS Prompt")

colors = constants.colors

try:
    dos_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except:
    print("Font file not found, using default.")
    dos_font = pygame.font.SysFont("monospace", FONT_SIZE)

# Reference: color block [████████]

def render_lines(lines, bg_color=colors["black"], text_color=colors["light_gray"]):
    screen.fill(bg_color)
    
    # Same regex: catches color;"text"
    token_pattern = re.compile(r'([a-zA-Z_]+);"([^"]*)"')

    for i, line in enumerate(lines):
        current_x = 2
        current_y = 2 + (i * FONT_SIZE)

        # 1. Trigger Check: Only parse if it starts with your command
        if line.startswith("COL_SHOW:"):
            # Remove the "COL_SHOW:" part to parse the rest
            content = line.replace("COL_SHOW:", "", 1).strip()
            
            matches = token_pattern.findall(content)
            
            if matches:
                for color_name, text in matches:
                    actual_color = colors.get(color_name.lower(), text_color)
                    text_surface = dos_font.render(text, True, actual_color)
                    screen.blit(text_surface, (current_x, current_y))
                    
                    # Move X forward (no extra space so you can control it in the quotes)
                    current_x += text_surface.get_width()
            else:
                # If COL_SHOW was used but no valid color tags were found
                text_surface = dos_font.render(content, True, text_color)
                screen.blit(text_surface, (current_x, current_y))
        
        else:
            # 2. Normal Line: Just render white text
            text_surface = dos_font.render(line, True, text_color)
            screen.blit(text_surface, (current_x, current_y))

    pygame.display.flip()

def wrap_text(text, font, max_width):
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word exceeds the max_width
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            # If current_line has content, save it and start a new one
            if current_line:
                wrapped_lines.append(current_line.strip())
            current_line = word + " "
    
    # Don't forget the last line
    if current_line:
        wrapped_lines.append(current_line.strip())
        
    return wrapped_lines


def bsod(code="0x0000003b", code_desc="SYSTEM_SERVICE_EXCEPTION"):
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

BSOD_COMMANDS = [
    "con\\con",
    "intl h int6h",
    "intl l int6h"
]

def dirlist():
    real_path = get_real_current_path()
    v_path_str = "\\".join(current_path)
    out = [f" Directory of C:\\{v_path_str}", ""]
    
    try:
        # Get all entries and convert to a list so we can sort them
        entries = list(os.scandir(real_path))
        
        # Grouping Logic: 
        # We sort by (is_file, name). Since False < True, 
        # Directories (is_file=False) will naturally come before Files (is_file=True).
        entries.sort(key=lambda e: (e.is_file(), e.name.lower()))

        for entry in entries:
            if entry.is_dir():
                out.append(f"{entry.name.upper():<12} <DIR>")
            else:
                size = entry.stat().st_size
                out.append(f"{entry.name.upper():<12} {size:>8} bytes")
                
    except FileNotFoundError:
        return ["Error: Current directory missing from disk."]
        
    # Footer
    stats = vfsinit.get_vfs_metadata()
    out.append("")
    out.append(f"{len([e for e in entries if not e.is_dir()]):>5} File(s) {stats['used']:>12} bytes")
    out.append(f"{len([e for e in entries if e.is_dir()]):>5} Dir(s)  {stats['free']:>12} bytes free")
    
    return out

def change_dir(args):
    if not args: 
        return f"C:\\{'\\'.join(current_path)}"
    
    target = args[0].lower()
    if target == "..":
        if current_path:
            current_path.pop()
        return None
    
    # Check if the folder exists physically
    potential_path = os.path.join(get_real_current_path(), target)
    if os.path.exists(potential_path) and os.path.isdir(potential_path):
        current_path.append(target)
    else:
        return "Invalid directory."

def cmd_type(args):
    if not args: return "Filename required."
    
    filename = args[0].lower()
    file_path = os.path.join(get_real_current_path(), filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as f:
            raw_lines = f.readlines()
            
        final_output = []
        for line in raw_lines:
            # Wrap each line from the file to fit the screen width
            wrapped = wrap_text(line.strip(), dos_font, 635)
            final_output.extend(wrapped)
        return final_output
    
    return "File not found."

def colortest_256():
    screen.fill(colors["black"])
    pygame.display.flip()
    sleep(0.5)
    bsod(code="0x00000116", code_desc="VIDEO_TDR_FAILURE")

def help():
    return [
        "Available commands:",
        "CLS - Clear the screen",
        "VER - Show version information",
        "SYSINFO - Display system information",
        "ECHO [text] - Display text",
        "DIR - List files and folders in current directory",
        "TYPE [filename] - Show contents of a file",
        "CD [folder] - Change directory",
        "DEL [filename] - Delete a file",
        "GPUTEST - Test GPU capabilities",
        "EDIT [filename] - Open file in editor",
        "STAT - Open statistic",
        "HELP - Show this help message",
        "EXIT - Shutdown this computer"
    ]

COMMANDS = {
    "cls": lambda args: [display_history.clear(), []][1],
    "ver": lambda args: [get_sys_info()["OS"]],
    "sysinfo": lambda args: [
        f"BIOS: {get_sys_info()['BIOS']}",
        f"CPU: {get_sys_info()['CPU']}",
        f"RAM: {get_sys_info()['RAM'] // 1024} KB",
        f"HDD Total: {vfsinit.get_vfs_metadata()['total'] // (1024*1024)} MB",
        f"HDD Free: {vfsinit.get_vfs_metadata()['free'] // (1024*1024)} MB"
    ],
    "echo": lambda args: [" ".join(args)],
    "dir": lambda args: dirlist(),
    "type": lambda args: cmd_type(args) if args else "Filename required.",
    "cd": lambda args: change_dir(args),
    "gputest/256color": lambda args: colortest_256(),
    "edit": lambda args: commands.editor(render_lines, screen, dos_font, colors, get_real_current_path(), args),
    "time": lambda args: display_history.append(commands.timetell()),
    "gputest": lambda args: commands.gputest(render_lines, colors),
    "del": lambda args: commands.delete(get_real_current_path(), args),
    "stat": lambda args: commands.stat(screen, colors),
    "help": lambda args: help()
}

def main():
    global display_history
    display_history = bios_post(screen, render_lines)

    install_file_path = os.path.join(constants.STORAGE_PATH, "install.txt")
    should_skip = os.path.exists(install_file_path)

    # Pass the skip boolean to your setup function
    commands.vsdos_setup(render_lines, colors, skip=should_skip)

    input_text = "" 

    pygame.display.set_caption("VS-DOS Prompt")
    
    while True:
        # 1. Update the Prompt based on current_path
        prompt_str = f"C:\\{'\\'.join(current_path)}> "
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    display_history.append(prompt_str + input_text)
                    
                    # DISPATCHER LOGIC
                    parts = input_text.strip().split()
                    if parts:
                        base = parts[0].lower()
                        args = parts[1:]
                        
                        if base in COMMANDS:
                            result = COMMANDS[base](args)
                            if isinstance(result, list): display_history.extend(result)
                            elif isinstance(result, str): display_history.append(result)
                        elif base in BSOD_COMMANDS:
                            if base == "con\\con":
                                bsod(code="0x0000003b", code_desc="SYSTEM_SERVICE_EXCEPTION")
                            else:
                                bsod(code="0x00000006", code_desc="INVALID_HANDLE")
                        elif base == "exit":
                            pygame.quit(); sys.exit()
                        else:
                            display_history.append(f"Bad command: {base}")
                            
                    input_text = "" # Clear for next command
                
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # 2. Render everything
        blink = "_" if int(time.time() * 2) % 2 == 0 else " "
        visible = display_history[-25:] + [prompt_str + input_text + blink]
        render_lines(visible)

if __name__ == "__main__":
    main()