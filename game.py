import math
import time
import pygame
import socketio

from config import *
from colors import *
import menu


def move_left_pad(amount):
    global LEFT_PAD_POSITION
    if (
            0
            < LEFT_PAD_POSITION[1] + amount
            < WINDOW_DIMENSIONS[1] - PAD_SIZE[1]):
        LEFT_PAD_POSITION = (
            LEFT_PAD_POSITION[0],
            LEFT_PAD_POSITION[1] + amount
        )

right_pad_moving_up = True

def move_right_pad():
    global RIGHT_PAD_POSITION, right_pad_moving_up
    # get next position for the right pad
    new_position = (
        RIGHT_PAD_POSITION[0],
        RIGHT_PAD_POSITION[1] + (
            RIGHT_PAD_MOVEMENT_SPEED if right_pad_moving_up else (
                - RIGHT_PAD_MOVEMENT_SPEED)
        )
    )
    if 0 < new_position[1] < WINDOW_DIMENSIONS[1] - PAD_SIZE[1]:
        RIGHT_PAD_POSITION = new_position
    else:
        right_pad_moving_up = not right_pad_moving_up

def move_ball():
    global BALL_POSITION, BALL_MOVEMENT_SPEED, score
    new_ball_position = (
        BALL_POSITION[0] + BALL_MOVEMENT_SPEED[0],
        BALL_POSITION[1] + BALL_MOVEMENT_SPEED[1]
    )

    # handle screen borders
    if (
            0 
            < new_ball_position[0] 
            < WINDOW_DIMENSIONS[0] - BALL_RADIUS / 2
            and 0
            < new_ball_position[1]
            < WINDOW_DIMENSIONS[1] - BALL_RADIUS / 2):
        BALL_POSITION = new_ball_position
    else:
        if new_ball_position[0] >= WINDOW_DIMENSIONS[0] - BALL_RADIUS / 2:
            score += 1
        BALL_POSITION = (
            WINDOW_DIMENSIONS[0] // 2,
            WINDOW_DIMENSIONS[1] // 2
        )
        BALL_MOVEMENT_SPEED = (10, 0)
    
    # handle right pad
    if (
        BALL_POSITION[0] >= RIGHT_PAD_POSITION[0] - BALL_RADIUS
        and RIGHT_PAD_POSITION[1] 
        <= BALL_POSITION[1]
        <= RIGHT_PAD_POSITION[1] + PAD_SIZE[1]
    ):
        BALL_MOVEMENT_SPEED = (
            -BALL_MOVEMENT_SPEED[0],
            BALL_MOVEMENT_SPEED[1] + (
                BALL_POSITION[1] - (
                    RIGHT_PAD_POSITION[1] + PAD_SIZE[1] // 2
                )
            ) // 16
        )

    # handle left pad
    if (
        BALL_POSITION[0] <= (
            LEFT_PAD_POSITION[0]
            + PAD_SIZE[0]
            + BALL_RADIUS
        )
        and LEFT_PAD_POSITION[1]
        <= BALL_POSITION[1]
        <= LEFT_PAD_POSITION[1] + PAD_SIZE[1]
    ):
        BALL_MOVEMENT_SPEED = (
            -BALL_MOVEMENT_SPEED[0],
            BALL_MOVEMENT_SPEED[1] + (
                BALL_POSITION[1] - (
                    LEFT_PAD_POSITION[1] + PAD_SIZE[1] // 2
                )
            ) // 16
        )

client_orientation = 'WRONG' # default
score = 0 # starting

def run_game_loop(master_address='localhost:5000'):
    sio = socketio.Client(logger=True)

    @sio.event
    def orient(data):
        print(data)
        global client_orientation
        client_orientation = data['data'].upper()
        print('Jolly good, I am {}!'.format(client_orientation))

    @sio.on('move_left_pad_down')
    def move_left_pad_down():
        move_left_pad(LEFT_PAD_MOVEMENT_SPEED)
    
    @sio.on('move_left_pad_up')
    def move_left_pad_up():
        move_left_pad(-LEFT_PAD_MOVEMENT_SPEED)
    
    @sio.on('speed_ball_up')
    def speed_ball_up():
        global BALL_MOVEMENT_SPEED

        ball_movement_speed_vector_size = math.sqrt(
            BALL_MOVEMENT_SPEED[0] ** 2
            + BALL_MOVEMENT_SPEED[1] ** 2
        )
        multiplier = 1 + BALL_MOVEMENT_SPEED_DELTA / (
            ball_movement_speed_vector_size
            or BALL_MOVEMENT_SPEED_DELTA + 1
        )
        if multiplier <= 0:
            multiplier = 0.5

        BALL_MOVEMENT_SPEED = (
            math.ceil(BALL_MOVEMENT_SPEED[0] * multiplier),
            math.ceil(BALL_MOVEMENT_SPEED[1] * multiplier),
        )

    @sio.on('speed_ball_down')
    def speed_ball_down():
        global BALL_MOVEMENT_SPEED

        ball_movement_speed_vector_size = math.sqrt(
            BALL_MOVEMENT_SPEED[0] ** 2
            + BALL_MOVEMENT_SPEED[1] ** 2
        )
        multiplier = 1 - BALL_MOVEMENT_SPEED_DELTA / (
            ball_movement_speed_vector_size
            or BALL_MOVEMENT_SPEED_DELTA + 1
        )
        if multiplier <= 0:
            multiplier = 0.5
        
        BALL_MOVEMENT_SPEED = (
            math.ceil(BALL_MOVEMENT_SPEED[0] * multiplier),
            math.ceil(BALL_MOVEMENT_SPEED[1] * multiplier),
        )
    
    sio.connect('http://' + master_address + ':5005')

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_DIMENSIONS, pygame.RESIZABLE)
    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()

    playing = True

    while playing:

        screen.fill(BLACK)
        if client_orientation in ('LEFT', 'WRONG'):
            # draw left pad
            pygame.draw.rect(screen, LIGHT_BLUE, (*LEFT_PAD_POSITION, *PAD_SIZE))
        if client_orientation in ('RIGHT', 'WRONG'):
            # draw right pad
            pygame.draw.rect(screen, GREEN, (*RIGHT_PAD_POSITION, *PAD_SIZE))
        # draw ball
        pygame.draw.circle(screen, WHITE, BALL_POSITION, BALL_RADIUS)
        
        # show menu
        screen.blit(
            menu.get_menu_surface(),
            (
                WINDOW_DIMENSIONS[0] // 2 - menu.MENU_SURFACE_SIZE[0] // 2,
                WINDOW_DIMENSIONS[1] - menu.MENU_SURFACE_SIZE[1] - 20
            )
        )

        # show score
        screen.blit(
            menu.get_score_surface(score),
            (
                WINDOW_DIMENSIONS[0] // 2 - menu.SCORE_SURFACE_SIZE[0] // 2,
                menu.SCORE_SURFACE_SIZE[1] // 2 + 20
            )
        )

        pygame.display.update()
        clock.tick(FPS)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if client_orientation == 'LEFT':
                sio.emit('left_slave_up')
            elif client_orientation == 'RIGHT':
                sio.emit('right_slave_up')

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if client_orientation == 'LEFT':
                sio.emit('left_slave_down')
            elif client_orientation == 'RIGHT':
                sio.emit('right_slave_down')
        
        move_right_pad()

        move_ball()
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT
                    or (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_q)):
                playing = False
                sio.disconnect()
                pygame.quit()
