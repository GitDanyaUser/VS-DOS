import sys
import pygame
import constants
import gui_stuff
from sound import play_beep
from utils import sleep
import time

colors = constants.colors

def get_sys_info():
    return {
        "BIOS": "Award Modular BIOS v6.00PG",
        "BIOS2": "Copyright (C) 1984-99, Award Software, Inc.",
        "VGABIOS": "S3 Trio64V Generic VGA BIOS (1.03-06)",
        "GPU": "S3 Trio64V+",
        "CPU": "I486DX4 100MHz(33x3)",
        "RAM": 8388608, #B
        "HDD": 512, #MB
        "OS": "VS-DOS 0.4 rev. 1"
    }

def bios_post(screen, render_lines):
    pygame.display.set_caption("Award Modular BIOS v6.00PG POST")
    info = get_sys_info()
    
    # Load and scale the logo
    eslogo = pygame.image.load("fonts/epa.png").convert_alpha()
    eslogo = pygame.transform.scale(eslogo, (160, 100))
    logo_rect = eslogo.get_rect(topright=(screen.get_width() - 10, 10))

    lines = [
        f"{info['BIOS']}, An Energy Star Ally",
        info["BIOS2"],
        "",
        "GREEN AGP/PCI/ISA/AMR SYSTEM",
        "",
        "Main Processor: " + info["CPU"],
        "Memory Testing: 0 KB OK",
        ""
    ]

    # Helper to keep the screen updated with the logo always blitted last
    def refresh():
        screen.fill((0, 0, 0))
        render_lines(lines)
        screen.blit(eslogo, logo_rect) # Logo is always drawn on top
        pygame.display.flip()

    # 1. RAM Test
    total_bytes = info["RAM"]
    step_bytes = 65536  # 64 KB per step
    
    for current_bytes in range(0, total_bytes + 1, step_bytes):
        lines[6] = f"Memory Testing: {current_bytes // 1024} KB OK"
        refresh()
        sleep(0.005)

    # Ensure final exact total KB is displayed
    lines[6] = f"Memory Testing: {total_bytes // 1024} KB OK"
    refresh()
    
    play_beep(frequency=1000, duration=200)

    # 2. Add Plug and Play info
    lines.extend([
        "Award Plug and Play BIOS Extension v1.0A",
        "Copyright (C) 1999, Award Software, Inc.",
        "",
        "Primary Master: Detecting..."
    ])
    refresh()
    
    sleep(0.5)
    
    # 3. HDD detection
    lines[11] = f"Primary Master: Fixed Disk {info['HDD']} MB"
    lines.extend([
        "Primary Slave: None", 
        "Secondary Master: None", 
        "Secondary Slave: None"
    ])
    refresh()
    
    sleep(1)
    lines.extend(["", "Starting VS-DOS..."])
    refresh()
    
    sleep(2)
    return [f"{info['OS']} - GPL-3.0 License, GitDanyaUser", ""]

def bios_setup(screen):
    #TODO: Add saving, loading and settings
    pygame.display.set_caption("CMOS Setup Utility - Copyright (C) 1984-1999 Award Software")
    
    BG_BLUE = (0, 0, 170)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 85)
    RED = (170, 0, 0)
    
    # Calculate RAM values from system info
    sys_info = get_sys_info()
    total_ram_kb = sys_info.get("RAM", 8388608) // 1024
    base_mem_kb = 640
    other_mem_kb = 384
    extended_mem_kb = max(0, total_ram_kb - 1024)
    
    try:
        font = pygame.font.Font("fonts/Px437_IBM_VGA_8x16.ttf", 16)
    except (FileNotFoundError, OSError):
        font = pygame.font.SysFont("monospace", 16, bold=True)
    
    LINE_H = 16
    INNER_WIDTH = 37
    char_w = 8

    current_screen = "MAIN"  # "MAIN", "STANDARD_CMOS"
    popup_type = None       # None, "QUIT_WITHOUT_SAVING", "SAVE_AND_EXIT"
    popup_input = "N"

    left_col = [
        ("Standard CMOS Features", True, "Standard CMOS Features Setup"),
        ("Advanced BIOS Features", True, "Advanced BIOS Features Setup"),
        ("Advanced Chipset Features", True, "Advanced Chipset Features Setup"),
        ("Integrated Peripherals", True, "Integrated Peripherals Setup"),
        ("Power Management Setup", True, "Power Management Setup"),
        ("PnP/PCI Configurations", True, "PnP/PCI Configurations")
    ]

    right_col = [
        ("PC Health Status", True, "PC Health Status Setup"),
        ("Load Fail-Safe Defaults", False, "Load Fail-Safe Defaults"),
        ("Load Optimized Defaults", False, "Load Optimized Defaults"),
        ("Set Password", False, "Change/Set/Disable Password"),
        ("Save & Exit Setup", False, "Save all CMOS changes to BIOS and Exit"),
        ("Exit Without Saving", False, "Abandon all CMOS changes and Exit")
    ]

    col, row = 0, 0
    clock = pygame.time.Clock()

    # Main menu border frame matrix
    border_lines = []
    border_lines.append("╔" + "═" * INNER_WIDTH + "╤" + "═" * INNER_WIDTH + "╗")
    for _ in range(15):
        border_lines.append("║" + " " * INNER_WIDTH + "│" + " " * INNER_WIDTH + "║")
    border_lines.append("╟" + "─" * INNER_WIDTH + "┼" + "─" * INNER_WIDTH + "╢")
    border_lines.append("║" + " " * INNER_WIDTH + "│" + " " * INNER_WIDTH + "║")
    border_lines.append("║" + " " * (INNER_WIDTH * 2 + 1) + "║")
    border_lines.append("╟" + "─" * (INNER_WIDTH * 2 + 1) + "╢")
    for _ in range(3):
        border_lines.append("║" + " " * (INNER_WIDTH * 2 + 1) + "║")
    border_lines.append("╚" + "═" * (INNER_WIDTH * 2 + 1) + "╝")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # POPUP CONTROLS
                if popup_type is not None:
                    if event.key == pygame.K_y:
                        pygame.quit()
                        sys.exit()  # Force immediate exit on Y key
                    elif event.key == pygame.K_n:
                        popup_type = None  # Cancel on N key
                    elif event.key == pygame.K_RETURN:
                        if popup_input == "Y":
                            pygame.quit()
                            sys.exit()
                        else:
                            popup_type = None
                    elif event.key == pygame.K_ESCAPE:
                        popup_type = None

                # MAIN MENU CONTROLS
                elif current_screen == "MAIN":
                    if event.key == pygame.K_F10:
                        popup_type = "SAVE_AND_EXIT"
                        popup_input = "Y"
                    elif event.key == pygame.K_ESCAPE:
                        popup_type = "QUIT_WITHOUT_SAVING"
                        popup_input = "N"
                    elif event.key == pygame.K_UP:
                        row = max(0, row - 1)
                    elif event.key == pygame.K_DOWN:
                        max_r = len(left_col) - 1 if col == 0 else len(right_col) - 1
                        row = min(max_r, row + 1)
                    elif event.key == pygame.K_LEFT:
                        if col == 1:
                            col = 0
                            row = min(row, len(left_col) - 1)
                    elif event.key == pygame.K_RIGHT:
                        if col == 0:
                            col = 1
                            row = min(row, len(right_col) - 1)
                    elif event.key == pygame.K_RETURN:
                        if col == 0 and row == 0:
                            current_screen = "STANDARD_CMOS"
                        elif col == 1 and row == 4:  # Save & Exit Setup
                            popup_type = "SAVE_AND_EXIT"
                            popup_input = "Y"
                        elif col == 1 and row == 5:  # Exit Without Saving
                            popup_type = "QUIT_WITHOUT_SAVING"
                            popup_input = "N"

                # STANDARD CMOS CONTROLS
                elif current_screen == "STANDARD_CMOS":
                    if event.key == pygame.K_ESCAPE:
                        current_screen = "MAIN"
                    elif event.key == pygame.K_F10:
                        popup_type = "SAVE_AND_EXIT"
                        popup_input = "Y"

        screen.fill(BG_BLUE)
        sw, sh = screen.get_width(), screen.get_height()

        # =========================================================
        # SCREEN 1: MAIN MENU
        # =========================================================
        if current_screen == "MAIN":
            title = font.render("CMOS Setup Utility - Copyright (C) 1984-1999 Award Software", True, WHITE)
            screen.blit(title, (sw // 2 - title.get_width() // 2, 8))

            y_start = 28
            x_frame = (sw - font.size(border_lines[0])[0]) // 2

            for i, line_str in enumerate(border_lines):
                line_surf = font.render(line_str, True, WHITE)
                screen.blit(line_surf, (x_frame, y_start + i * LINE_H))

            for c_idx, col_items in enumerate([left_col, right_col]):
                x_start = x_frame + (char_w * 3 if c_idx == 0 else (INNER_WIDTH + 4) * char_w)
                
                for r_idx, (text, has_arrow, _) in enumerate(col_items):
                    y_pos = y_start + (r_idx * 2 + 1) * LINE_H
                    is_selected = (col == c_idx and row == r_idx)
                    
                    if has_arrow:
                        arrow_surf = font.render("► ", True, YELLOW)
                        screen.blit(arrow_surf, (x_start, y_pos))

                    text_x = x_start + (arrow_surf.get_width() if has_arrow else 0)

                    if is_selected:
                        txt_surf = font.render(text, True, WHITE, RED)
                    else:
                        txt_surf = font.render(text, True, YELLOW)
                        
                    screen.blit(txt_surf, (text_x, y_pos))

            y_mid = y_start + 16 * LINE_H
            screen.blit(font.render("Esc : Quit", True, WHITE), (x_frame + char_w * 3, y_mid + LINE_H))
            screen.blit(font.render("↑ ↓ → ← : Select Item", True, WHITE), (x_frame + (INNER_WIDTH + 4) * char_w, y_mid + LINE_H))
            screen.blit(font.render("F10 : Save & Exit Setup", True, WHITE), (x_frame + char_w * 3, y_mid + 2 * LINE_H))

            y_lower = y_start + 19 * LINE_H
            curr_desc = left_col[row][2] if col == 0 else right_col[row][2]
            desc_lbl = font.render(curr_desc, True, WHITE)
            screen.blit(desc_lbl, (sw // 2 - desc_lbl.get_width() // 2, y_lower + 2 * LINE_H))

        # =========================================================
        # SCREEN 2: STANDARD CMOS FEATURES SUBMENU
        # =========================================================
        elif current_screen == "STANDARD_CMOS":
            header1 = font.render("CMOS Setup Utility - Copyright (C) 1984-1999 Award Software", True, WHITE)
            header2 = font.render("Standard CMOS Features", True, WHITE)
            screen.blit(header1, (sw // 2 - header1.get_width() // 2, 6))
            screen.blit(header2, (sw // 2 - header2.get_width() // 2, 22))

            W_CHARS, H_LINES = 76, 23
            box_top    = "╔" + "═" * W_CHARS + "╗"
            box_mid    = "║" + " " * W_CHARS + "║"
            box_bottom = "╚" + "═" * W_CHARS + "╝"

            x_box = (sw - font.size(box_top)[0]) // 2
            y_box = 40

            screen.blit(font.render(box_top, True, WHITE), (x_box, y_box))
            for i in range(1, H_LINES):
                screen.blit(font.render(box_mid, True, WHITE), (x_box, y_box + i * LINE_H))
            screen.blit(font.render(box_bottom, True, WHITE), (x_box, y_box + H_LINES * LINE_H))

            # Header (White)
            hd_head = "HARD DISKS           TYPE      SIZE   CYLS HEAD PRECOMP LANDZ SECTOR  MODE"
            screen.blit(font.render(hd_head, True, WHITE), (x_box + 16, y_box + 5 * LINE_H))
            screen.blit(font.render("─" * 74, True, WHITE), (x_box + 16, y_box + 6 * LINE_H))

            t_str = time.strftime("%a, %b %d %Y")
            tm_str = time.strftime("%H : %M : %S")
            screen.blit(font.render("Date (mm:dd:yy) : " + t_str, True, WHITE), (x_box + 16, y_box + 2 * LINE_H))
            screen.blit(font.render("Time (hh:mm:ss) : " + tm_str, True, WHITE), (x_box + 16, y_box + 3 * LINE_H))

            disks = ["Primary Master", "Primary Slave", "Secondary Master", "Secondary Slave"]
            for d_idx, d_name in enumerate(disks):
                d_line = f"{d_name:<19}: Auto         0      0    0       0     0      0  AUTO"
                screen.blit(font.render(d_line, True, YELLOW), (x_box + 16, y_box + (7 + d_idx) * LINE_H))

            screen.blit(font.render("Drive A : 1.44M, 3.5 in.", True, YELLOW), (x_box + 16, y_box + 12 * LINE_H))
            screen.blit(font.render("Drive B : None", True, YELLOW), (x_box + 16, y_box + 13 * LINE_H))
            screen.blit(font.render("Floppy 3 Mode Support : Disabled", True, YELLOW), (x_box + 16, y_box + 14 * LINE_H))
            screen.blit(font.render("Video   : EGA/VGA", True, YELLOW), (x_box + 16, y_box + 16 * LINE_H))
            screen.blit(font.render("Halt On : All Errors", True, YELLOW), (x_box + 16, y_box + 17 * LINE_H))

            # Memory Panel Box
            mem_x = x_box + 390
            mem_y = y_box + 12 * LINE_H
            screen.blit(font.render("┌──────────────────────────┐", True, WHITE), (mem_x, mem_y))
            screen.blit(font.render(f"│ Base Memory:      {base_mem_kb:>5}K │", True, WHITE), (mem_x, mem_y + LINE_H))
            screen.blit(font.render(f"│ Extended Memory:  {extended_mem_kb:>5}K │", True, WHITE), (mem_x, mem_y + 2 * LINE_H))
            screen.blit(font.render(f"│ Other Memory:     {other_mem_kb:>5}K │", True, WHITE), (mem_x, mem_y + 3 * LINE_H))
            screen.blit(font.render("├──────────────────────────┤", True, WHITE), (mem_x, mem_y + 4 * LINE_H))
            screen.blit(font.render(f"│ Total Memory:     {total_ram_kb:>5}K │", True, WHITE), (mem_x, mem_y + 5 * LINE_H))
            screen.blit(font.render("└──────────────────────────┘", True, WHITE), (mem_x, mem_y + 6 * LINE_H))

            # Footer
            screen.blit(font.render("─" * W_CHARS, True, WHITE), (x_box + 8, y_box + 19 * LINE_H))
            screen.blit(font.render("ESC : Quit                ↑ ↓ → ← : Select Item        PU/PD/+/- : Modify", True, WHITE), (x_box + 16, y_box + 20 * LINE_H))
            screen.blit(font.render("F1  : Help                (Shift)F2 : Change Color", True, WHITE), (x_box + 16, y_box + 21 * LINE_H))

        # =========================================================
        # OVERLAY MODALS: QUIT OR SAVE POPUPS
        # =========================================================
        if popup_type is not None:
            pop_w, pop_h = 42, 5
            pop_top    = "╔" + "═" * pop_w + "╗"
            pop_mid    = "║" + " " * pop_w + "║"
            pop_bottom = "╚" + "═" * pop_w + "╝"

            px = (sw - pop_w * char_w) // 2
            py = (sh - pop_h * LINE_H) // 2 - 10

            pop_rect = pygame.Rect(px, py, (pop_w + 2) * char_w, (pop_h + 1) * LINE_H)
            pygame.draw.rect(screen, RED, pop_rect)

            screen.blit(font.render(pop_top, True, WHITE, RED), (px, py))
            for h_idx in range(1, pop_h):
                screen.blit(font.render(pop_mid, True, WHITE, RED), (px, py + h_idx * LINE_H))
            screen.blit(font.render(pop_bottom, True, WHITE, RED), (px, py + pop_h * LINE_H))

            if popup_type == "SAVE_AND_EXIT":
                msg = f" SAVE to CMOS and EXIT (Y/N)? {popup_input} "
            else:
                msg = f" Quit Without Saving (Y/N)? {popup_input} "

            msg_surf = font.render(msg, True, WHITE, RED)
            screen.blit(msg_surf, (sw // 2 - msg_surf.get_width() // 2, py + 2 * LINE_H))

        pygame.display.flip()
        clock.tick(30)