import os
import pygame
from colors import WHITE, BLACK

MENU_SURFACE_SIZE = (250, 50)
MENU_ALPHA = 128  # 0 to 255

def get_menu_surface():
    menu_surface = pygame.Surface(MENU_SURFACE_SIZE)
    menu_surface.fill(WHITE)
    menu_surface.set_alpha(MENU_ALPHA)
    font = pygame.font.Font(os.path.abspath('./fonts/tron.ttf'), 10)
    text_top = font.render("Q to quit", 1, BLACK)
    text_bottom = font.render("W, S, up, down to control", 1, BLACK)
    text_top_size = text_top.get_size()
    text_bottom_size = text_bottom.get_size()
    menu_surface.blit(
        text_top,
        (
            MENU_SURFACE_SIZE[0] / 2 - text_top_size[0] / 2,
            MENU_SURFACE_SIZE[1] / 4 - text_top_size[1] / 2,
        )
    )
    menu_surface.blit(
        text_bottom,
        (
            MENU_SURFACE_SIZE[0] / 2 - text_bottom_size[0] / 2,
            3 * MENU_SURFACE_SIZE[1] / 4 - text_bottom_size[1] / 2,
        )
    )
    return menu_surface
