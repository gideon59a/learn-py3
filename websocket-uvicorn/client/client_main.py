import asyncio
import aiohttp
from aiohttp import BasicAuth, client_exceptions
import threading
import traceback
import logging

from client_ops import ClientOps

SERVER_BASE_URL = f'http://localhost:8000'
my_token = 'abcd12345'
RETRY_INTERVAL = 2
RETRY_NUMBER = 10
WS_WAIT_TIMEOUT_ON_INPUT = 10

LOG_FILE_FORMAT = '%(asctime)s MY_PREFIX [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
LOG_CONSOLE_FORMAT = '%(module)s - %(message)s'
logging.basicConfig(filename='client.log', level=logging.DEBUG, format=LOG_FILE_FORMAT)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter(LOG_CONSOLE_FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(ch)
logger.info("Logger started.")

global_ws_connection = None

ws_wait_timeout = 10
ws_timeout_change_event = asyncio.Event()


class GracefulExit(Exception):
    # Triggers program closing
    pass


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None
        self._running = True

    async def init_session(self):
        self.session = aiohttp.ClientSession()
        logger.debug(f"Http session created: {self.session}")

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
                    logger.debug(f"Response Code: {response.status}")
                    if response.status == 200 or response.status == 202:
                        return await response.json()
                    else:
                        logger.error(f"Got unexpected status {response.status}: {await response.text()}")
            except aiohttp.ClientError as e:
                traceback.print_exc()
                logger.debug(f"Request failed: {e}, retrying in {RETRY_INTERVAL} seconds...")
                ###############await asyncio.sleep(RETRY_INTERVAL)
                raise
        logger.error(f"Failed to communicate after {retries} attempts.")
        return None

    async def get(self, endpoint, username=None, password=None, **kwargs):
        return await self._request("GET", endpoint, username, password, **kwargs)

    async def post(self, endpoint, json_data=None, username=None, password=None, **kwargs):
        return await self._request("POST", endpoint, username, password, json=json_data, **kwargs)

    async def close(self):
        logger.debug(f"Closing the http client session {self.session} ...")
        if self.session:
            await self.session.close()
            self.session = None

    def stop(self):
        logger.debug("GOT STOP event")
        self._running = False

    def is_running(self):
        return self._running


class WebSocketClient:

    def __init__(self):
        self.ws = None

    async def websocket_listener(self, ws_token, event, http_client, client_ops):
        """
        :param ws_token: The token that identifies the specific client
        :param event: Set the event to notify that the message has been processed (triggering waiting for a new user input)
        :param http_client: Just for checking whether the client is still running
        :return:
        """
        global ws_wait_timeout

        # The below while is for server disconnection cases, where the client has to try to reconnect
        # Note that once the ws connection is established, http reconnection doesn't affect the websocket connection
        retries = RETRY_NUMBER
        while http_client.is_running() and retries > 0:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                    async with session.ws_connect(f'ws://localhost:8000/ws?token={ws_token}') as ws:
                        self.ws = ws
                        retries = RETRY_NUMBER
                        while True:  # This inner loop will keep the connection alive for multiple messages
                            msg = await ws.receive()
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                logger.debug(f"Received WebSocket message: {msg.data}")
                                result = client_ops.process_server_message(msg.data)
                                logger.debug(f"The result status of the ws operation: {result['status']}")
                                logger.debug("... Setting the event to continue receiving user inputs")
                                event.set()  # Notify that the message is processed
                            elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                                logger.error(f"GOT websocket disconnection. Message is {msg.type}")
                                break  # Break the inner loop to try reconnecting

            except aiohttp.client_exceptions.ClientConnectorError:
                traceback.print_exc()
                retries -= 1
                logger.error(f"Failed to connect to server for websocket. Retrying in {RETRY_INTERVAL} seconds..., "
                             f"retries left: {retries}/{RETRY_NUMBER}")
                await asyncio.sleep(RETRY_INTERVAL)
        msg = "Exit either due to no http_client running or due to ws disconnect with no retries left"
        http_client.stop()
        raise GracefulExit(msg)

    def close_websocket(self):
        if self.ws:
            # Close the ws connection
            asyncio.create_task(self.ws.close())


async def user_input_handler(queue, event, http_client, client_ops):
    while http_client.is_running():
        logger.debug("Waiting for a message from the websocket before continuing")
        logger.debug("ASYNC WAITING for the event to be set (before getting a new input)")
        await event.wait()
        logger.debug("AFTER event.wait")
        logger.debug("ASYNC WAITING for queue.get.")
        logger.info("Please enter a command 'lp' 'sp' or 'g'  (or 'exit' to quit): ")
        cmd = await queue.get()
        logger.debug("AFTER queue.get")

        logger.info("Process user input")
        op_result = await client_ops.process_user_input(cmd)
        logger.info(f"User processing result is: {op_result}")

        if op_result["action"] == "to_exit":
            http_client.stop()
            raise GracefulExit("********* Got exit request via user input!")
        elif op_result["action"] == "to_clear_event":
            logger.debug("Clearing the event as we're waiting for a new WebSocket message before getting the next input"
                         " from the user")
            event.clear()


def input_thread(queue, loop, http_client):
    while True and http_client.is_running():
        cmd = input("ASYNC WAITING for input from user. : \n")
        logger.debug(f"(DEBUG) Receiving input: {cmd}")
        asyncio.run_coroutine_threadsafe(queue.put(cmd), loop)


async def basic_http_check(client):
    # Testing GET and POST methods
    response_get = await client.get("/is_alive")
    logger.debug(f"GET response: {response_get}")
    response_get = await client.get("/is_alive_auth", username='my_username', password="my_password")
    logger.debug(f"GET response: {response_get}")


async def main(http_client):
    """The purpose is to support two async processes simultaneously:
          1. Receive user inputs (via the keyboard in this case, or via GUI in other cases)
          2. Get messages from the server via the ws connection. """

    #http_client = Client(SERVER_BASE_URL)
    await http_client.init_session()
    client_ops = ClientOps(my_token, http_client, logger)

    # Initiates
    input_queue = asyncio.Queue()  # For user keyboard inputs

    event = asyncio.Event()  # The event will trigger listening to user inputs
    event.set()  # Initially set the event so that we can get user input

    # Async use a separated thread, so the below plus the above input_thread allow the input thread to communicate
    # with the async one

    threading.Thread(target=input_thread, args=(input_queue, loop, http_client), daemon=True).start()

    # Create tasks and use gather on these tasks
    #websocket_listener = WebSocketClient().websocket_listener()
    websocket_client = WebSocketClient()

    try:
        task1 = asyncio.create_task(websocket_client.websocket_listener(my_token, event, http_client, client_ops))
        task2 = asyncio.create_task(user_input_handler(input_queue, event, http_client, client_ops))
        await asyncio.gather(task1, task2)
    except (KeyboardInterrupt, GracefulExit) as e:
        logger.error(f"Exception, close program due to:  {e}")
    except Exception as e:
        logger.error(f"Error in asyncio: {e}")
        traceback.print_exc()
    finally:
        websocket_client.close_websocket()
        # await http_client.close()  # No need for that here, as it appears that should be closed using event loop.


if __name__ == '__main__':
    http_client = HttpClient(SERVER_BASE_URL)
    logger.debug(f"http_client session: {http_client.session}")

    # Async use a separated thread, so the below plus the above input_thread allow the input thread to communicate
    # with the async one
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main(http_client))
    except (KeyboardInterrupt, GracefulExit):  # When ctrl-c is pressed, SIGINT raises this exception.
        logger.info("Shutting down gracefully...")
        # http_client.stop()  # No need to close here, as closed by main.
    finally:
        logger.info("Shutting down gracefully. "
                    f"Closing http_client session: {http_client.session} and asyncio event loop...")
        loop.run_until_complete(http_client.close())
        loop.close()
