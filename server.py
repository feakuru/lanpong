import csv
import math
import socketio
from datetime import datetime
from aiohttp import web

from config import (
    FPS,
    LEFT_PAD_POSITION,
    RIGHT_PAD_POSITION,
    LEFT_PAD_MOVEMENT_SPEED,
    RIGHT_PAD_MOVEMENT_SPEED,
    WINDOW_DIMENSIONS,
    PAD_SIZE,
    BALL_POSITION,
    BALL_MOVEMENT_SPEED,
    BALL_MOVEMENT_SPEED_DELTA,
    BALL_RADIUS,
)

right_pad_moving_up = True
score = 0


def move_ball():
    global BALL_POSITION, BALL_MOVEMENT_SPEED, score
    new_ball_position = (
        BALL_POSITION[0] + BALL_MOVEMENT_SPEED[0],
        BALL_POSITION[1] + BALL_MOVEMENT_SPEED[1]
    )

    # handle screen borders
    if (
            0 > new_ball_position[1]
            or new_ball_position[1] > WINDOW_DIMENSIONS[1] - BALL_RADIUS / 2):
        BALL_MOVEMENT_SPEED = (
            BALL_MOVEMENT_SPEED[0],
            - BALL_MOVEMENT_SPEED[1]
        )
    if (
            0
            < new_ball_position[0] 
            < WINDOW_DIMENSIONS[0] - BALL_RADIUS / 2):
        BALL_POSITION = new_ball_position
    else:
        if new_ball_position[0] >= WINDOW_DIMENSIONS[0] - BALL_RADIUS:
            score += 1
        BALL_POSITION = (
            RIGHT_PAD_POSITION[0] - BALL_RADIUS * 2,
            RIGHT_PAD_POSITION[1] + PAD_SIZE[1] // 2
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


def sign(x):
    return -1 if x < 0 else 1


def speed_ball_up():
    global BALL_MOVEMENT_SPEED

    BALL_MOVEMENT_SPEED = (
        math.ceil(BALL_MOVEMENT_SPEED[0] * 1.1) or sign(BALL_MOVEMENT_SPEED[0]),
        math.ceil(BALL_MOVEMENT_SPEED[1] * 1.2) or sign(BALL_MOVEMENT_SPEED[1]),
    )

def speed_ball_down():
    global BALL_MOVEMENT_SPEED
    
    BALL_MOVEMENT_SPEED = (
        math.ceil(BALL_MOVEMENT_SPEED[0] * 0.9) or sign(BALL_MOVEMENT_SPEED[0]),
        math.ceil(BALL_MOVEMENT_SPEED[1] * 0.8) or sign(BALL_MOVEMENT_SPEED[1]),
    )


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


def run_server():
    with open('log.csv', 'w', newline='') as logfile:
        log_writer = csv.writer(logfile)
        sio = socketio.AsyncServer(logger=True)

        slaves = []

        @sio.event
        async def connect(sid, environ):
            slaves.append(sid)
            if len(slaves) == 1:
                await sio.emit('orient', {'data': 'left'}, room=sid)
                print('Connected to left slave {}'.format(sid))
            elif len(slaves) == 2:
                await sio.emit('orient', {'data': 'right'}, room=sid)
                await sio.emit('start')
                print('Connected to right slave {}'.format(sid))
            else:
                print(
                    'Got {} slaves, dunno what to do with them, '
                    'will only work on first two'.format(
                        len(slaves)
                    )
                )
            return 200, 'OK'
        
        @sio.event
        async def disconnect(sid):
            # Do this if you want to break the left/right logic on disconnect
            # slaves.remove(sid)
            print('Client {} disconnected.'.format(sid))

        @sio.on('left_slave_up')
        async def move_left_pad_up(sid):
            log_writer.writerow([str(datetime.now()), 'move_left_pad_up'])
            move_left_pad(LEFT_PAD_MOVEMENT_SPEED)
            await sio.emit('move_left_pad', {'position': LEFT_PAD_POSITION})
            return 200, "OK"

        @sio.on('left_slave_down')
        async def move_left_pad_down(sid):
            await sio.emit('move_left_pad_down')
            log_writer.writerow([str(datetime.now()), 'move_left_pad_down'])
            move_left_pad(-LEFT_PAD_MOVEMENT_SPEED)
            await sio.emit('move_left_pad', {'position': LEFT_PAD_POSITION})
            return 200, "OK"

        async def move_right_pad():
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
            await sio.emit('move_right_pad', {'position': RIGHT_PAD_POSITION})

        @sio.on('tick')
        async def tick(sid):
            await move_right_pad()
            move_ball()
            await sio.emit(
                'set_ball_position',
                {'position': BALL_POSITION}
            )
            await sio.emit('set_score', {'score': score})

        @sio.on('right_slave_up')
        async def right_slave_up(sid):
            speed_ball_up()
            log_writer.writerow([str(datetime.now()), 'speed_ball_up'])
            return 200, "OK"

        @sio.on('right_slave_down')
        async def right_slave_down(sid):
            speed_ball_down()
            log_writer.writerow([str(datetime.now()), 'speed_ball_down'])
            return 200, "OK"

        app = web.Application()
        sio.attach(app)
        web.run_app(app, host='127.0.0.1', port='5005')
