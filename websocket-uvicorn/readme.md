# Introduction
## Purpose
- a python server that can serve several clients concurrently
  - rest interface with websocket support
- a python client that can concurrently end endlessly: 
  - Listen to user (keyborad) requests and send requests to the server.
  - Listen to server messages using websocket interface and process them.

## Client behaviour
The client is asynchronously listening to both the keyboard and the websocket connection with the server.
The process:
The client gets user command from the keyboard. As a result it may send a http post request to the server /my_endpoint4 
The server may respond eiter with 202 or with another status code.
The client reads and processes the server response, and as a result it will print a message to the user console,
and may either wait for a new user command, or for a message the server sends via the websocket.
So if the client gets a message via the websocket, it will process it, may send a message to the user console,
and then wait for a new command from the user.



## Packages
- asyncio: The server as well as the client uses asyncio for supporting websocket & user inputs concurrently with the rest api.
- fastapi: Modern (comparing to flask), out of the box support of websocket, docs, etc. Supported by uvicorn.
- uvicron: supports ASGI, similar to gunicorn (which is for synchronous web servers)



# Technical consideration



## Input from keyboard
As there is no support for input command in the async lib, the following would create a blocking while waiting for user input:  
      async def user_input_task():
         while True:
             input("Press Enter to trigger the endpoint (type 'exit' to quit): ")
             print("> Client triggering the /my_endpoint3 endpoint...")
             await get_http(f'/my_endpoint3?ws_token={my_token}')
    
while in main we would have:
     # Start WebSocket listener task but don't await
     asyncio.create_task(listen_ws())

Therefore, threading (by ThreadPoolExecutor) was used instead.

