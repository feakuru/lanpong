import os
import pygame
from colors import WHITE, BLACK

MENU_SURFACE_SIZE = (250, 50)
SCORE_SURFACE_SIZE = (100, 50)
MENU_ALPHA = 200  # 0 to 255

def get_menu_surface():
    menu_surface = pygame.Surface(MENU_SURFACE_SIZE)
    menu_surface.fill(WHITE)
    menu_surface.set_alpha(MENU_ALPHA)
    
    font = pygame.font.Font(os.path.abspath('./fonts/tron.ttf'), 10)
    
    text_top = font.render("Q to quit", 1, BLACK)
    text_bottom = font.render("W, S / up, down to control", 1, BLACK)
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


def get_score_surface(score):
    score_surface = pygame.Surface(SCORE_SURFACE_SIZE)
    score_surface.fill(WHITE)
    score_surface.set_alpha(MENU_ALPHA)
    
    font = pygame.font.Font(os.path.abspath('./fonts/tron.ttf'), 24)
    
    score_text = font.render(str(score), 1, BLACK)
    score_text_size = score_text.get_size()
    
    score_surface.blit(
        score_text,
        (
            SCORE_SURFACE_SIZE[0] / 2 - score_text_size[0] / 2,
            SCORE_SURFACE_SIZE[1] // 2 - score_text_size[1] / 2,
        )
    )

    return score_surface
