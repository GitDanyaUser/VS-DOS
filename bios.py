import sys
import time
import winsound
import pygame
import constants
from sound import play_beep

colors = constants.colors

def get_sys_info():
    return {
        "BIOS": "Award Modular BIOS v6.00PG",
        "BIOS2": "Copyright (C) 1984-99, Award Software, Inc.",
        "VGABIOS": "S3 Trio64V Generic VGA BIOS (1.03-06)",
        "GPU": "S3 Trio64V+",
        "CPU": "I486DX4 100MHz(33x3)",
        "RAM": 64000, #B
        "HDD": 512, #MB
        "OS": "VS-DOS Beta 3 rev. 1"
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
    for i in range(0, info["RAM"] + 1, 4096):
        lines[6] = f"Memory Test: {i} KB OK"
        refresh()
        time.sleep(0.05)
    
    play_beep(frequency=1000, duration=500)

    # 2. Add Plug and Play info
    lines.extend([
        "Award Plug and Play BIOS Extension v1.0A",
        "Copyright (C) 1999, Award Software, Inc.",
        "",
        "Primary Master: Detecting..."
    ])
    refresh()
    
    time.sleep(0.5)
    
    # 3. HDD detection
    lines[11] = f"Primary Master: Fixed Disk {info['HDD']} MB"
    lines.extend([
        "Primary Slave: None", 
        "Secondary Master: None", 
        "Secondary Slave: None"
    ])
    refresh()
    
    time.sleep(1)
    lines.extend(["", "Starting VS-DOS..."])
    refresh()
    
    time.sleep(2)
    return [f"{info['OS']} - MIT License, GitDanyaUser", ""]

def bios_setup(screen, render_lines):
    pygame.display.set_caption("Award Modular BIOS v6.00PG Setup Utility")

    def draw_text_centered(text, center):
        font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        text_surf = font.render(text, True, colors["white"])
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)
    
    lines = [
        "ROM PCI/ISA BIOS (2A69HQ1A)",
        "CMOS SETUP UTILITY",
        "AWARD SOFTWARE, INC.",
        "",
        " STANDARD CMOS SETUP           INTEGRATED PERIPHERALS",
        " BIOS FEATURES SETUP           PC HEALTH STATUS",
        " CHIPSET FEATURES SETUP        LOAD FAIL-SAFE DEFAULTS",
        " POWER MANAGEMENT SETUP        LOAD OPTIMIZED DEFAULTS",
        " PNP/PCI CONFIGURATION         SET PASSWORD",
        " LOAD BIOS DEFAULTS            SAVE & EXIT SETUP",
        " LOAD SETUP DEFAULTS           EXIT WITHOUT SAVING",
        "",
        " Esc : Quit                    ↑ ↓ → ← : Select Item",
        " F10 : Save & Exit Setup       (Shift)F2 : Change Color"
    ]

    running = True
    show_confirm = False

    while running:
        screen.fill(colors["blue"])
        render_lines(lines, bg_color=colors["blue"], text_color=colors["white"])

        if show_confirm:
            # Create a simple red confirmation box overlay
            overlay_rect = pygame.Rect(0, 0, 400, 100)
            overlay_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            
            # Draw box shadow then the box
            pygame.draw.rect(screen, colors["black"], overlay_rect.move(5, 5)) 
            pygame.draw.rect(screen, colors["red"], overlay_rect)
            pygame.draw.rect(screen, colors["white"], overlay_rect, 2) # Border

            # Render the prompt text
            # Assuming your render_lines can take an optional offset or custom positioning
            # For simplicity, we'll use a basic prompt message:
            confirm_msg = "SAVE to CMOS and EXIT (Y/N)?  "
            # (You might need a small helper here to draw text at a specific coordinate)
            draw_text_centered(confirm_msg, overlay_rect.center)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if not show_confirm:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_F10:
                        play_beep(frequency=800, duration=50) # Tiny feedback beep
                        show_confirm = True
                else:
                    # Logic for the confirmation box
                    if event.key == pygame.K_y:
                        running = False # Exit setup
                    if event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        show_confirm = False # Go back to menu
    pygame.quit()
    sys.exit()