import asyncio
import aiohttp
from aiohttp import BasicAuth, client_exceptions
import threading
import signal
import traceback


SERVER_BASE_URL = f'http://localhost:8000'

my_token = '12345'
RETRY_INTERVAL = 2
RETRY_NUMBER = 10

class GracefulExit(Exception):
    print(f"*********** GracefulExit(Exception) **********")
    pass


class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()
        self._running = True

    @staticmethod
    def _auth(username, password):
        auth = None
        if username and password:
            auth = BasicAuth(username, password)
        return auth

    async def _request(self, method, endpoint, username=None, password=None, retries=RETRY_NUMBER, **kwargs):
        auth = self._auth(username, password)
        for retry in range(retries):
            try:
                async with self.session.request(method, f"{self.base_url}{endpoint}", auth=auth, **kwargs) as response:
                    print(f"Response Code: {response.status}")
                    if response.status == 200 or response.status == 202:
                        return await response.json()
                    else:
                        print(f"Got unexpected status {response.status}: {await response.text()}")
            except aiohttp.ClientError as e:
                traceback.print_exc()
                print(f"Request failed: {e}, retrying in {RETRY_INTERVAL} seconds...")
                ###############await asyncio.sleep(RETRY_INTERVAL)
                raise
        print(f"Failed to communicate after {retries} attempts.")
        return None

    async def get(self, endpoint, username=None, password=None, **kwargs):
        return await self._request("GET", endpoint, username, password, **kwargs)

    async def post(self, endpoint, json_data=None, username=None, password=None, **kwargs):
        return await self._request("POST", endpoint, username, password, json=json_data, **kwargs)

    async def close(self):
        print("Closing the client...")
        if self.session:
            await self.session.close()
            self.session = None

    def stop(self):
        print("GOT STOP event")
        self._running = False

    def is_running(self):
        return self._running


async def websocket_listener(ws_token, event, http_client):
    """
    :param ws_token: The token that identifies the specific client
    :param event: Set the event to notify that the message has been processed (triggering waiting for a new user input)
    :param http_client: Just for checking whether the client is still running
    :return:
    """
    # The below while is for server disconnection cases, where the client has to try to reconnect
    # Note that once the ws connection is established, http reconnection doesn't affect the websocket connection
    retries = RETRY_NUMBER
    while http_client.is_running() and retries > 0:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.ws_connect(f'ws://localhost:8000/ws?token={ws_token}') as ws:
                    retries = RETRY_NUMBER
                    while True:  # This inner loop will keep the connection alive for multiple messages
                        msg = await ws.receive()
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            print(f"Received WebSocket message: {msg.data}")
                            print(f"Processing server ws message........................")
                            print("... Setting the event to continue receiving user inputs")
                            event.set()  # Notify that the message is processed
                        elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            print(f"GOT websocket disconnection. Message is {msg.type}")
                            break  # Break the inner loop to try reconnecting

        except aiohttp.client_exceptions.ClientConnectorError:
            traceback.print_exc()
            retries -= 1
            print(f"Failed to connect to server for websocket. Retrying in {RETRY_INTERVAL} seconds..., "
                  f"retry {retries}/{RETRY_NUMBER}")
            await asyncio.sleep(RETRY_INTERVAL)


async def user_input_handler(queue, event, http_client):
    while http_client.is_running():
        print("Waiting for a message from the websocket before continuing")
        print("ASYNC WAITING for the event to be set (before getting a new input)")
        await event.wait()
        print("AFTER event.wait")
        print("ASYNC WAITING for queue.get.")
        print("Please enter a command 'lp' 'sp' or 'g'  (or 'exit' to quit): ")
        cmd = await queue.get()
        print("AFTER queue.get")

        print("Process user input")
        if cmd.strip() == "exit":
            raise GracefulExit("********* Got exit request!")
            #break
        elif cmd.strip():
            data = {
                "key": "cmd",
                "value": cmd
            }
            print("ASYNC WAITING for http")

            to_clear_event = True if 'l' in cmd else False
            if 'p' in cmd:
                endpoint = '/my_endpoint4'
                await http_client.post(f'{endpoint}?ws_token={my_token}', json_data=data)
            elif 'g' in cmd:
                endpoint = '/my_endpoint3'
                await http_client.get(f'{endpoint}?ws_token={my_token}')
            else:
                pass
            print("AFTER HTTP")
            if to_clear_event:
                print("Clearing the event as we're waiting for a new WebSocket message before getting the next input "
                      "from the user")
                event.clear()
        else:
            print("Unknown command, re-enter command")


def input_thread(queue, loop, http_client):
    while True and http_client.is_running():
        cmd = input("ASYNC WAITING for input from user. : \n")
        print(f"(DEBUG) Receiving input: {cmd}")
        asyncio.run_coroutine_threadsafe(queue.put(cmd), loop)


async def basic_http_check(client):
    # Testing GET and POST methods
    response_get = await client.get("/is_alive")
    print(f"GET response: {response_get}")
    response_get = await client.get("/is_alive_auth", username='my_username', password="my_password")
    print(f"GET response: {response_get}")


async def main(http_client):
    """The purpose is to support two async processes simultaneously:
          1. Receive user inputs (via the keyboard in this case, or via GUI in other cases)
          2. Get messages from the server via the ws connection. """

    #http_client = Client(SERVER_BASE_URL)

    # Initiates
    input_queue = asyncio.Queue()  # For user keyboard inputs

    event = asyncio.Event()  # The event will trigger listening to user inputs
    event.set()  # Initially set the event so that we can get user input

    # Async use a separated thread, so the below plus the above input_thread allow the input thread to communicate
    # with the async one

    threading.Thread(target=input_thread, args=(input_queue, loop, http_client), daemon=True).start()

    # Create tasks and use gather on these tasks
    try:
        task1 = asyncio.create_task(websocket_listener(my_token, event, http_client))
        task2 = asyncio.create_task(user_input_handler(input_queue, event, http_client))
        await asyncio.gather(task1, task2)
    except Exception as e:
        print(f"Error in asyncio: {e}")
        traceback.print_exc()
    finally:
        await http_client.close()


if __name__ == '__main__':
    http_client = Client(SERVER_BASE_URL)

    # Async use a separated thread, so the below plus the above input_thread allow the input thread to communicate
    # with the async one
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main(http_client))
    except (KeyboardInterrupt, GracefulExit):  # When ctrl-c is pressed, SIGINT raises this exception.
        print("Shutting down gracefully...")
        http_client.stop()
        traceback.print_exc()
    finally:
        loop.run_until_complete(http_client.close())
        loop.close()

        asyncio.run(http_client.close())
