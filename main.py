import pygame
import sys
import os
import time
from bios import get_sys_info, bios_post
import constants
import re
import vfsinit

FONT_PATH = constants.FONT_PATH
FONT_SIZE = constants.FONT_SIZE
VFS_PATH = vfsinit.VFS_PATH

vfsinit.init_vfs()
vfs = vfsinit.load_vfs()
vfsinit.update_used_space(vfs)
vfsinit.save_vfs(vfs)
current_path = [] # C:\

def get_cur_node():
    # This tells Python to look for the variables defined outside the function
    node = vfs
    for folder in current_path:
        if folder in node["folders"]:
            node = node["folders"][folder]
    return node

pygame.init()

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

bsod_commands = [
    "con\\con",
    "intl h int6h",
    "intl l int6h"
]

def dirlist():
    node = get_cur_node()
    out = [f" Directory of C:\\" + "\\".join(current_path), ""]
    
    # List Folders
    for fld in node.get("folders", {}):
        out.append(f"{fld.upper():<12} <DIR>")
    
    # List Files - fdata is just a string now!
    for fname, fdata in node.get("files", {}).items():
        size = len(str(fdata))
        out.append(f"{fname.upper():<12} {size:>8} bytes")
        
    return out

def change_dir(args):
    if not args: return f"C:\\{'\\'.join(current_path)}"
    target = args[0].lower()
    node = get_cur_node()
    
    if target == "..":
        if current_path: current_path.pop()
    elif target in node["folders"]:
        current_path.append(target)
    else:
        return "Invalid directory."

def cmd_type(args):
    if not args: return "Filename required."
    
    filename = args[0].lower()
    node = get_cur_node()
    
    if filename in node["files"]:
        content = node["files"][filename]
        return content.split("\n")
    
    return "File not found."

def colortest():
    color_names = constants.get_color_names()
    lines = ["== IBM VGA 16 Color Test =="]
    for color in color_names:
        lines.append(f'COL_SHOW:{color};"████████ {color.upper()}"')
    lines.append("============================")
    return lines

def colortest_256():
    screen.fill(colors["black"])
    pygame.display.flip()
    time.sleep(0.5)
    bsod(code="0x00000116", code_desc="VIDEO_TDR_FAILURE")

def editor(args):
    # TODO: Implement in Beta 3
    return "We're sorry, but the editor is not implemented, modify filestorage.json directly."

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
        "COLORTEST - Display color test blocks",
        "EDITOR [filename] - Open file in editor (Not Implemented)",
        "HELP - Show this help message",
        "EXIT - Shutdown this computer"
    ]

COMMANDS = {
    "cls": lambda args: [display_history.clear(), []][1],
    "ver": lambda args: [get_sys_info()["OS"]],
    "sysinfo": lambda args: [
        f"BIOS: {get_sys_info()['BIOS']}",
        f"CPU: {get_sys_info()['CPU']}",
        f"RAM: {get_sys_info()['RAM']} KB",
        f"HDD: {get_sys_info()['HDD']} MB"
    ],
    "echo": lambda args: [" ".join(args)],
    "dir": lambda args: dirlist(),
    "type": lambda args: cmd_type(args) if args else "Filename required.",
    "cd": lambda args: change_dir(args),
    "colortest": lambda args: display_history.append("Make sure your monitor supports 16 colors!") or render_lines(display_history) or time.sleep(3) or colortest(),
    "colortest/256color": lambda args: display_history.append("Make sure your monitor supports 256 colors!") or render_lines(display_history) or time.sleep(3) or colortest_256(),
    "editor": lambda args: editor(args),
    "help": lambda args: help()
}

def main():
    global display_history
    display_history = bios_post(screen, render_lines)
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
                        elif base in bsod_commands:
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