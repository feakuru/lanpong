import pygame
from colors import WHITE

MENU_SURFACE_SIZE = (200, 50)
MENU_ALPHA = 128  # 0 to 255

def get_menu_surface():
    menu_surface = pygame.Surface(MENU_SURFACE_SIZE)
    menu_surface.fill(WHITE)
    menu_surface.set_alpha(MENU_ALPHA)
    return menu_surface
