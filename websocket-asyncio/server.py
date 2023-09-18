# server.py

import asyncio
import websockets
from aiohttp import web
import time


async def http_handler(request):
    return web.Response(text="Hello from HTTP!")

async def do_my_stuff1_handler(request):
    time.sleep(10)
    return web.Response(text="You've accessed /do_my_stuff1 endpoint!")

async def do_my_stuff2_handler(request):
    time.sleep(10)
    return web.Response(text="You've accessed /do_my_stuff2 endpoint!")

async def ws_handler(websocket, path):
    # This can be used to push messages to the client
    await asyncio.sleep(5)
    await websocket.send("Message from server!")


def main():
    # WebSocket server
    ws_server = websockets.serve(ws_handler, "localhost", 8765)

    # HTTP server
    app = web.Application()
    app.router.add_get('/', http_handler)
    app.router.add_get('/do_my_stuff1', do_my_stuff1_handler)
    app.router.add_get('/do_my_stuff2', do_my_stuff2_handler)
    runner = web.AppRunner(app)
    loop = asyncio.get_event_loop()

    # Run servers
    loop.run_until_complete(runner.setup())
    http_server = web.TCPSite(runner, 'localhost', 8080)

    loop.run_until_complete(http_server.start())
    loop.run_until_complete(ws_server)
    loop.run_forever()

if __name__ == '__main__':
    main()
