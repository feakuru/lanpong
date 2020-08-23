import math
import time
import pygame
import socketio

from config import *
from colors import *
import menu

client_orientation = 'WRONG' # default
score = 0 # starting
playing = False

def run_game_loop(
        master_address='localhost:5000',
        override_show_left_pad=False,
        override_hide_ball=False,
        override_show_right_pad=False,
        ):
    global playing
    sio = socketio.Client(logger=True)

    @sio.event
    def orient(data):
        global client_orientation
        client_orientation = data['data'].upper()
        print('Initialized as the {} pad!'.format(client_orientation))

    @sio.event
    def start():
        global playing
        playing = True

    @sio.on('move_left_pad')
    def move_left_pad(data):
        global LEFT_PAD_POSITION
        LEFT_PAD_POSITION = data['position']

    @sio.on('move_right_pad')
    def move_right_pad(data):
        global RIGHT_PAD_POSITION
        RIGHT_PAD_POSITION = data['position']

    @sio.on('set_ball_speed')
    def set_ball_speed(data):
        global BALL_MOVEMENT_SPEED
        BALL_MOVEMENT_SPEED = data['speed']

    @sio.on('set_ball_position')
    def set_ball_position(data):
        global BALL_POSITION
        BALL_POSITION = data['position']

    @sio.on('set_score')
    def set_score(data):
        global score
        score = data['score']

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
        if (
            BALL_MOVEMENT_SPEED[0] == 0
            and BALL_MOVEMENT_SPEED[1] == 0):
            BALL_MOVEMENT_SPEED = (
                int(math.ceil(math.sqrt(BALL_MOVEMENT_SPEED_DELTA))),
                int(math.ceil(math.sqrt(BALL_MOVEMENT_SPEED_DELTA))),
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

    while not playing:
        clock.tick(FPS) # waiting for start event

    while playing:

        screen.fill(BLACK)
        if client_orientation in ('LEFT', 'WRONG') or override_show_left_pad:
            # draw left pad
            pygame.draw.rect(screen, LIGHT_BLUE, (*LEFT_PAD_POSITION, *PAD_SIZE))
        if client_orientation in ('RIGHT', 'WRONG') or override_show_right_pad:
            # draw right pad
            pygame.draw.rect(screen, GREEN, (*RIGHT_PAD_POSITION, *PAD_SIZE))
        if not override_hide_ball:
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

        if client_orientation == 'RIGHT':
            sio.emit('tick')

        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT
                    or (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_q)):
                playing = False
                sio.disconnect()
                pygame.quit()
