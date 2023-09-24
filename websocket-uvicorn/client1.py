# client.py

import asyncio
import aiohttp
import websockets
import time
from concurrent.futures import ThreadPoolExecutor


start = time.time()
my_token = '12345'


async def get_http(path='/'):
    async with aiohttp.ClientSession() as session:
        print(f"Time before sending to path {path}: {time.time() - start}")
        async with session.get(f'http://localhost:8000{path}') as response:
            print(f"Response Code: {response.status}")
            print("Response text:" + await response.text())  # response.text is a coroutine to support non-blocking
                                                             # when the received message is very long
            print(f"-------------------Time after path {path} is {time.time() - start}")


async def process_server_message(message: str):
    # Do something with the message from the server
    print(f"Client processing the following message received from the server via websocket:   {message}")
    time.sleep(1)
    # Add more processing logic here if needed
    print(f"Processing the message {message}  ****DONE****")


async def listen_ws(token=my_token):
    uri = f"ws://localhost:8000/ws?token={token}"
    async with websockets.connect(uri) as websocket:
        print("> Client WebSocket connection established!")
        while True:
            message = await websocket.recv()
            print(f"< {message}")
            await process_server_message(message)


async def post_http(endpoint, json_data):
    url = f"http://localhost:8000{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            print(f"Response Code: {response.status}")
            print(await response.text())



def blocking_input(prompt: str) -> str:
    return input(prompt)


executor = ThreadPoolExecutor()
async def async_input(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, blocking_input, prompt)


async def user_input_task():
    while True:
        ii = await async_input("Press Enter to trigger the endpoint (type 'exit' to quit): ")
        print(f"got {ii} from user")
        if ii == '3':
            print("> Client triggering the /my_endpoint3 endpoint...")
            await get_http(f'/my_endpoint3?ws_token={my_token}')
        elif ii == '4':
            print("> Client triggering the /my_endpoint4 endpoint...")
            data = {"key": "my_cmd", "value": "cmd4"}
            await post_http(f'/my_endpoint4?ws_token={my_token}', data)


async def main():
    """The purpose is to support two async processes simultaneously:
      1. Receive user inputs (via the keyboard in this case, or via GUI in other cases)
      2. Get messages from the server via the ws connection. """

    # Start both tasks
    asyncio.create_task(listen_ws())
    asyncio.create_task(user_input_task())

    # Keep the main routine running to keep both tasks alive
    while True:
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
