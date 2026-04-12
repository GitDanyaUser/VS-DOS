import time
import winsound
import pygame

def get_sys_info():
    return {
        "BIOS": "Award Modular BIOS v6.00PG, An Energy Star Ally",
        "BIOS2": "Copyright (C) 1984-99, Award Software, Inc.",
        "VGABIOS": "Phoenix Technologies Ltd. VGA BIOS v1.0",
        "CPU": "I486DX4 100MHz(33x3)",
        "RAM": 64000, 
        "HDD": 512
    }

def bios_post(screen, render_lines):
    pygame.display.set_caption("Award Modular BIOS v6.00PG POST")
    info = get_sys_info()
    
    # Load and scale the logo
    eslogo = pygame.image.load("fonts/epa.png").convert_alpha()
    eslogo = pygame.transform.scale(eslogo, (150, 100))
    logo_rect = eslogo.get_rect(topright=(screen.get_width() - 10, 10))

    lines = [
        info["BIOS"],
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
    
    winsound.Beep(1000, 500)

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
    return ["VS-DOS Beta 2 rev. 1 - MIT License, GitDanyaUser", ""]