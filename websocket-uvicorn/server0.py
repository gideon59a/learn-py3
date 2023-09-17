# server.py

from fastapi import FastAPI, WebSocket, BackgroundTasks
import asyncio
from fastapi.responses import JSONResponse
import time
start = time.time()

app = FastAPI()

connected_clients = []

async def do_my_stuff(ws_token: str):
    await asyncio.sleep(5)  # Simulating a long-running task
    for client in connected_clients:
        print("Send a message to the WebSocket that initiated the request")
        for client in connected_clients:
            if client.scope.get("query_string") == f"token={ws_token}".encode():
                await client.send_text(f"Task triggered by you is done! Time: {time.time() - start}")

        # Broadcast a status update to all WebSocket connections
        for client in connected_clients:
            await client.send_text(f"Broadcasting: Task triggered by client {ws_token} is done!  Time: {time.time() - start}")

@app.get("/my_endpoint1")
def endpoint1():
    return {"message": "You accessed endpoint 1!"}

@app.get("/my_endpoint2")
def endpoint2():
    return {"message": "You accessed endpoint 2!"}

# The below is not proper because status_code 200 returns instead of 202. See /my_endpoint4 for proper implementation
@app.get("/my_endpoint3wrong")
def endpoint3_wrong(background_tasks: BackgroundTasks):
    background_tasks.add_task(do_my_stuff)
    return {"message": "my_endpoint3 is In progress"}, 202

@app.get("/my_endpoint3")
def endpoint3(ws_token: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(do_my_stuff, ws_token)
    return JSONResponse(content={"message": "In progress"}, status_code=202)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # keep the connection open
    except:
        connected_clients.remove(websocket)


# One way of running is externally using the linux command:     # uvicorn server:app --workers 2"
# The other way is to run as shown below, which seems to me more "programmatically"
# Note that uvicorn.Server is used below rather than uvicorn.run that doesn't have the workers attribute.
if __name__ == '__main__':
    import uvicorn
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, workers=2)
    server = uvicorn.Server(config)
    server.run()


