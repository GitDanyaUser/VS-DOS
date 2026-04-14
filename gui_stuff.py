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
FONT_PATH = constants.FONT_PATH
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

def draw_window(surface, title, x, y, w, h, close=True):
    # Main Window Body
    pygame.draw.rect(surface, colors["light_gray"], (x, y, w, h))
    pygame.draw.rect(surface, colors["black"], (x, y, w, h), 1) # Thin border
    
    # Title Bar
    pygame.draw.rect(surface, colors["blue"], (x+2, y+2, w-4, 20))
    title_surf = win_font.render(title, True, colors["white"])
    surface.blit(title_surf, (x + 5, y + 4))
    
    # Close Button (The little minus sign in 3.1)
    if close:
        pygame.draw.rect(surface, colors["light_gray"], (x+w-20, y+4, 16, 16))
        pygame.draw.rect(surface, colors["black"], (x+w-20, y+4, 16, 16), 1)
        pygame.draw.line(surface, colors["black"], (x+w-16, y+12), (x+w-8, y+12), 2)

def draw_window2(surface, title, x, y, w, h, close=True):
    # Main Window Body
    pygame.draw.rect(surface, colors["light_gray"], (x, y, w, h))
    
    # Title Bar
    pygame.draw.rect(surface, colors["black"], (x+2, y+2, w-4, 20))
    title_surf = win_font.render(title, True, colors["white"])
    surface.blit(title_surf, (x + 5, y + 4))
    
    # Close Button
    if close:
        closex = win_font.render("X", True, colors["light_red"])
        surface.blit(closex, (x+w-20, y+4, 16, 16))