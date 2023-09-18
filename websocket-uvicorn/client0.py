# client.py

import asyncio
import aiohttp
import websockets
import time
start = time.time()

my_token = '12345'

async def get_http(path='/'):
    async with aiohttp.ClientSession() as session:
        print(f"Time before sending to path {path}: {time.time() - start}")
        async with session.get(f'http://localhost:8000{path}') as response:
            print(f"Response Code: {response.status}")
            print(await response.text())
            print(f"-------------------Time after path {path} is {time.time() - start}")


async def listen_ws(token=my_token):
    uri = f"ws://localhost:8000/ws?token={token}"
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(f"< {greeting}")

        # Sending a message to the WebSocket server
        await websocket.send("Hello Server!")
        response = await websocket.recv()
        print(f"<<< {response}")


async def main():
    print(f"Time at main start: {time.time() - start}")
    #await get_http('/my_endpoint1')
    #await get_http('/my_endpoint2')
    await get_http(f'/my_endpoint3?ws_token={my_token}')
    await listen_ws()
    print(f"Time at main end: {time.time() - start}")

asyncio.run(main())
