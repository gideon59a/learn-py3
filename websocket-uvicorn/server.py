# server.py

from fastapi import FastAPI, WebSocket, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

import asyncio
from pydantic import BaseModel
import time
import uuid

start = time.time()

app = FastAPI()
security = HTTPBasic()


# The pydantic BaseModel defines below a data model named Item,
# which helps in automatically validating the incoming JSON data.
# In the app.post that get json within the client request, FastAPI will automatically parse the incoming JSON into
# the Item model. If the incoming data doesn't fit the model, FastAPI will send a 422 Unprocessable Entity response
# back to the client with details on what's wrong.
class Item(BaseModel):
    key: str
    value: str


connected_clients = []


async def do_my_stuff(ws_token: str):
    await asyncio.sleep(2)  # Simulating a long-running task
    for client in connected_clients:
        print("Send a message to the WebSocket that initiated the request")
        for client in connected_clients:
            if client.scope.get("query_string") == f"token={ws_token}".encode():
                await client.send_text(f"Unicast: Task triggered by you is done! Time: {time.time() - start}")

        # Broadcast a status update to all WebSocket connections
        #for client in connected_clients:
        #    await client.send_text(f"Broadcasting: Task triggered by client {ws_token} is done!  Time: {time.time() - start}")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "my_username")
    correct_password = secrets.compare_digest(credentials.password, "my_password")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


@app.get("/is_alive")
def is_alive():
    return {"message": "Server is alive. No auth."}

@app.get("/is_alive_auth")
def status(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return {"message": "Client successfully authenticated by the server."}

@app.get("/get_token")
def get_token():
    # Generate a unique token using UUID
    token = str(uuid.uuid4())
    return {"ws_token": token}

@app.get("/private-endpoint")
def read_private(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return {"message": "Hello, authenticated user!"}


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
    print(f"A short get request")
    return JSONResponse(content={"server message": "okay"}, status_code=200)


@app.post("/my_endpoint4")
async def post_endpoint(item: Item, ws_token: str = None, background_tasks: BackgroundTasks = None):
    print(f"Received data: {item.key} = {item.value}, ws_token: {ws_token}")
    cmd = item.value
    if 'l' in cmd:
        print(f"A long POST request")
        print(f"Will run for ws_token {ws_token} the background_tasks: {background_tasks}")
        if ws_token and background_tasks:
            background_tasks.add_task(do_my_stuff, ws_token)
        return JSONResponse(content={"server message": f"Long command: {cmd} received from client"}, status_code=202)
    else:  # Immediate answer
        print(f"A short POST request")
        return JSONResponse(content={"server message": f"Short command: {cmd} received from client"}, status_code=200)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # keep the connection open
            print(f"ws data received by server: {data}")
    except:
        connected_clients.remove(websocket)


# One way of running is externally using the linux command:     # uvicorn server:app --workers 2"
# The other way is to run as shown below, which seems to me more "programmatically"
# Note that uvicorn.Server is used below rather than uvicorn.run that doesn't have the workers attribute.
if __name__ == '__main__':
    import uvicorn
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, workers=2, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
