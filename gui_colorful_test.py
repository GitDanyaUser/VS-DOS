import pygame
import sys
import os
import constants

# --- Constants & Colors ---
colors = constants.colors

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Windows 3.1 Color Test")

# Load Font
FONT_PATH = os.path.join("fonts", "Px437_IBM_VGA_8x16.ttf")
try:
    win_font = pygame.font.Font(FONT_PATH, 16)
    big_font = pygame.font.Font(FONT_PATH, 20)
    small_font = pygame.font.Font(FONT_PATH, 12)
except:
    win_font = pygame.font.SysFont("Arial", 16, bold=True)
    big_font = pygame.font.SysFont("Arial", 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 12)

def draw_button(surface, text, x, y, w, h, pressed=False):
    # Button Shadow/Highlight logic
    top_color = colors["light_gray"] if pressed else colors["white"]
    bot_color = colors["white"] if pressed else colors["dark_gray"]
    
    pygame.draw.rect(surface, colors["light_gray"], (x, y, w, h))
    pygame.draw.line(surface, top_color, (x, y), (x+w, y), 2)
    pygame.draw.line(surface, top_color, (x, y), (x, y+h), 2)
    pygame.draw.line(surface, bot_color, (x, y+h), (x+w, y+h), 2)
    pygame.draw.line(surface, bot_color, (x+w, y), (x+w, y+h), 2)
    
    text_surf = small_font.render(text, True, colors["black"])
    text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
    surface.blit(text_surf, text_rect)

def draw_window(surface, title, x, y, w, h):
    # Main Window Body
    pygame.draw.rect(surface, colors["light_gray"], (x, y, w, h))
    pygame.draw.rect(surface, colors["black"], (x, y, w, h), 1) # Thin border
    
    # Title Bar
    pygame.draw.rect(surface, colors["blue"], (x+2, y+2, w-4, 20))
    title_surf = win_font.render(title, True, colors["white"])
    surface.blit(title_surf, (x + 5, y + 4))
    
    # Close Button (The little minus sign in 3.1)
    pygame.draw.rect(surface, colors["light_gray"], (x+w-20, y+4, 16, 16))
    pygame.draw.rect(surface, colors["black"], (x+w-20, y+4, 16, 16), 1)
    pygame.draw.line(surface, colors["black"], (x+w-16, y+12), (x+w-8, y+12), 2)

def main():
    btn_pressed = False
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicking the "OK" button
                if 270 <= mouse_pos[0] <= 370 and 300 <= mouse_pos[1] <= 330:
                    btn_pressed = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if btn_pressed:
                    print("OK Clicked!")
                    btn_pressed = False

        # --- Rendering ---
        screen.fill(colors["light_cyan"])
        
        # Draw a "Program Manager" style window
        draw_window(screen, "VS-DOS Default Manager", 120, 100, 400, 250)
        
        # Draw some content inside the window
        msg = small_font.render("System Color Palette Diagnostic", True, colors["black"])
        screen.blit(msg, (140, 135))

        msg2 = win_font.render("This text will be coloured red", True, colors["red"])
        screen.blit(msg2, (140, 220))
        msg3 = win_font.render("This text will be coloured green", True, colors["green"])
        screen.blit(msg3, (140, 240))
        msg4 = win_font.render("This text will be coloured blue", True, colors["blue"])
        screen.blit(msg4, (140, 260))

        # Draw small color swatches (Visualizing your colors dict)
        swatch_colors = [colors["light_red"], colors["light_green"], colors["light_blue"], colors["yellow"], colors["light_magenta"], colors["light_cyan"]]
        for i, color in enumerate(swatch_colors):
            pygame.draw.rect(screen, color, (140 + (i*50), 160, 40, 40))
            pygame.draw.rect(screen, colors["black"], (140 + (i*50), 160, 40, 40), 1)

        # Draw interactive button
        draw_button(screen, "OK", 270, 300, 100, 30, btn_pressed)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()