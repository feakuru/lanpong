import pygame
from colors import WHITE

MENU_SURFACE_SIZE = (200, 150)

def get_menu_surface():
    menu_surface = pygame.Surface(MENU_SURFACE_SIZE)
    menu_surface.fill(WHITE)
    menu_surface.set_alpha(128)  # 0 to 255
