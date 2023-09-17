# client.py

import asyncio
import aiohttp
import websockets
import time

async def get_http(path='/'):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8080{path}') as response:
            print(f"Response Code: {response.status}")
            print(await response.text())
            print("-------------------")

async def listen_ws():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        print(f"< Received: {message}")

async def main():
    await get_http()
    print(f"Time before stuff1 is {time.time() - start}")
    await get_http('/do_my_stuff1')
    print(f"Time before stuff2 is {time.time() -start }")
    await get_http('/do_my_stuff2')
    await listen_ws()

start = time.time()
asyncio.run(main())
end = time.time()
print(f"Elasped time: {end-start}")
