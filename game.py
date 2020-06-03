import pygame

from config import *
from colors import *
import menu


def move_left_pad(amount):
    global LEFT_PAD_POSITION
    if 0 < LEFT_PAD_POSITION[1] + amount < WINDOW_DIMENSIONS[1] - PAD_SIZE[1]:
        LEFT_PAD_POSITION = (LEFT_PAD_POSITION[0], LEFT_PAD_POSITION[1] + amount)


def move_right_pad(amount):
    global RIGHT_PAD_POSITION
    if 0 < RIGHT_PAD_POSITION[1] + amount < WINDOW_DIMENSIONS[1] - PAD_SIZE[1]:
        RIGHT_PAD_POSITION = (RIGHT_PAD_POSITION[0], RIGHT_PAD_POSITION[1] + amount)


# Actual game code starts here

pygame.init()

screen = pygame.display.set_mode(WINDOW_DIMENSIONS, pygame.RESIZABLE)
pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

playing = True

while playing:

    screen.fill(BLACK)
    # draw pad 1
    pygame.draw.rect(screen, LIGHT_BLUE, (*LEFT_PAD_POSITION, *PAD_SIZE))
    # draw pad 2
    pygame.draw.rect(screen, GREEN, (*RIGHT_PAD_POSITION, *PAD_SIZE))
    pygame.display.update()
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_left_pad(-MOVEMENT_SPEED)
    elif keys[pygame.K_s]:
        move_left_pad(MOVEMENT_SPEED)
    if keys[pygame.K_UP]:
        move_right_pad(-MOVEMENT_SPEED)
    elif keys[pygame.K_DOWN]:
        move_right_pad(MOVEMENT_SPEED)

    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT
                or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_q)):
            pygame.quit()
            playing = False
        
    
