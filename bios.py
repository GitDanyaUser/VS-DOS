import sys
import pygame
import constants
from sound import play_beep
from utils import sleep

colors = constants.colors

def get_sys_info():
    return {
        "BIOS": "Award Modular BIOS v6.00PG",
        "BIOS2": "Copyright (C) 1984-99, Award Software, Inc.",
        "VGABIOS": "S3 Trio64V Generic VGA BIOS (1.03-06)",
        "GPU": "S3 Trio64V+",
        "CPU": "I486DX4 100MHz(33x3)",
        "RAM": 128000, #B
        "HDD": 512, #MB
        "OS": "VS-DOS 0.2 rev. 1"
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
        sleep(0.02)
    
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

def bios_setup(screen, render_lines):
    #TODO: Add saving, loading, changing settings and styling
    pygame.display.set_caption("Award Modular BIOS v6.00PG Setup")
    top_lines = [
        "CMOS Setup Utility - Copyright (C) 1984-1999 Award Software",
        "MODDED - REMOVE STYLING" # Styling is hard to do
    ]
    
    def choose(available_opts):
        selected = 0
        while True:
            render_lines(top_lines + [""] + [f"{'>' if i == selected else ' '} {opt}" for i, opt in enumerate(available_opts)], bg_color=colors["blue"], text_color=colors["white"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(available_opts)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(available_opts)
                    elif event.key == pygame.K_RETURN:
                        return available_opts[selected]

    options = [
        "Standard CMOS Features",
        "Advanced BIOS Features",
        "Advanced Chipset Features",
        "Power Management Setup",
        "PnP/PCI Configurations",
        "PC Health Status",
        "Frequency/Voltage Control",
        "Load Fail-Safe Defaults",
        "Load Optimized Defaults",
        "Set Supervisor Password",
        "Set User Password",
        "Save & Exit Setup",
        "Exit Without Saving"
    ]
    while True:
        choice = choose(options)
        if choice == "Exit Without Saving":
            __import__("main").main()
        elif choice == "Save & Exit Setup":
            __import__("main").main()