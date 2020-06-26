import socketio
from aiohttp import web

def run_server():
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
        await sio.emit('move_left_pad_up')
        return 200, "OK"


    @sio.on('left_slave_down')
    async def move_left_pad_down(sid):
        await sio.emit('move_left_pad_down')
        return 200, "OK"


    @sio.on('right_slave_up')
    async def speed_ball_up(sid):
        await sio.emit('speed_ball_up')
        return 200, "OK"


    @sio.on('right_slave_down')
    async def speed_ball_down(sid):
        await sio.emit('speed_ball_down')
        return 200, "OK"

    app = web.Application()
    sio.attach(app)
    web.run_app(app, host='127.0.0.1', port='5005')
