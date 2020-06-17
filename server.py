import socketio
from aiohttp import web

def run_server():
    sio = socketio.AsyncServer(async_mode='aiohttp')
    # TODO index ehlo

    @sio.on('left_slave_up')
    def move_left_pad_up(sid, data):
        sio.emit('move_left_pad_up', {})
        return 200, "OK"


    @sio.on('left_slave_down')
    def move_left_pad_down(sid, data):
        sio.emit('move_left_pad_down', {})
        return 200, "OK"


    @sio.on('right_slave_up')
    def speed_ball_up(sid, data):
        sio.emit('speed_ball_up', {})
        return 200, "OK"


    @sio.on('right_slave_down')
    def speed_ball_down(sid, data):
        sio.emit('speed_ball_down', {})
        return 200, "OK"

    app = web.Application()
    sio.attach(app)
    web.run_app(app)
