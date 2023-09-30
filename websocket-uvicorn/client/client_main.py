import asyncio
import uuid

import aiohttp
from aiohttp import BasicAuth, client_exceptions
import threading
import traceback
import logging
import os

from client_ops import ClientOps

SERVER_BASE_URL = f'http://localhost:8000'
RETRY_INTERVAL = 2
RETRY_NUMBER = 10
WS_WAIT_TIMEOUT_ON_INPUT = 10

LOG_FILE_FORMAT = '%(asctime)s MY_PREFIX [%(module)-15.15s] [%(levelname)-6.6s]  %(message)s'
LOG_CONSOLE_FORMAT = '%(module)s - %(message)s'
log_file_path = os.path.join(os.getcwd(), 'client.log')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format=LOG_FILE_FORMAT)
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
                    logger.debug(f"Response Code (at _request): {response.status}")
                    if response.status == 200 or response.status == 202:
                        return await response.json(), response.status
                    else:
                        logger.error(f"Got unexpected status {response.status}: {await response.text()}")
            except aiohttp.ClientError as e:
                traceback.print_exc()
                logger.debug(f"Request failed: {e}, retrying in {RETRY_INTERVAL} seconds...")
                raise
        logger.error(f"Failed to communicate after {retries} attempts.")
        return None, None

    async def get(self, endpoint, username=None, password=None, **kwargs):
        print(f"GOT get req to: {endpoint} ")
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

    async def websocket_listener(self, ws_token, listen_to_user_event, http_client, client_ops):
        """
        :param ws_token: The token that identifies the specific client
        :param listen_to_user_event: Set the event to notify that the message has been processed (triggering waiting for a new user input)
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
                                listen_to_user_event.set()  # Notify that the message is processed
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


async def user_input_handler(queue, listen_to_user_event, http_client, client_ops):
    """
    User keyboard inputs are handled provided that listen_to_user_event is set.
    Once the user input is processed, per its result either the listen_to_user_event state is kept so new user inputs
    are processed, or the listen_to_user_event is cleared for waiting for the server to respond via the websocket.
    :param queue:
    :param event:
    :param http_client:
    :param client_ops:
    :return:
    """
    while http_client.is_running():
        logger.debug("Waiting for a message from the websocket before continuing")
        logger.debug("ASYNC WAITING for the event to be set (before getting a new input)")
        await listen_to_user_event.wait()
        logger.debug("AFTER event.wait")
        logger.debug("ASYNC WAITING for queue.get.")
        logger.info(client_ops.print_request_from_user())
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
            listen_to_user_event.clear()


def input_thread(user_input_queue, events_loop, listen_to_user_event, http_client):
    """
    On any new user input, enter this input into the user input queue.
    Note that this thread just puts the user commands into the queue but doesn't process them.

    :param user_input_queue:
    :param events_loop: async events loop
    :param listen_to_user_event
    :param http_client: This thread runs endlessly, but on closing the program the http_client is closed and this is
                        used as an indication to close this thread too.
    :return:
    """
    while True and http_client.is_running():
        cmd = input("ASYNC WAITING for input from either user or server. "
                    "Enter 'cont' to force processing user inputs: \n")
        logger.debug(f"(DEBUG) Receiving input: {cmd}")
        if "cont" in cmd:
            listen_to_user_event.set()  # Force continuing with listening even if user_input_handler is still waiting
                                        # for a ws message from the server
        asyncio.run_coroutine_threadsafe(user_input_queue.put(cmd), events_loop)


async def basic_http_check(http_client):
    # Testing GET and POST methods
    logger.debug("***** Sever http get access sanity check:")
    response_get, return_code1 = await http_client.get("/is_alive")
    logger.debug(f"GET response: {response_get} {return_code1}")
    response_get, return_code2 = await http_client.get("/is_alive_auth", username='my_username', password="my_password")
    logger.debug(f"GET response: {response_get} {return_code2}")
    if return_code1 != 200 or return_code2 != 200:
        msg = "ERROR: Sever http get access sanity check FAILED, exiting"
        logger.error(msg)
        raise msg
    logger.debug("------- check ended.")


async def main(http_client, events_loop):
    """The purpose is to support two async processes simultaneously:
          1. Receive user inputs (via the keyboard in this case, or via GUI in other cases)
          2. Get messages from the server via the ws connection. """

    await http_client.init_session()

    # Just a sanity check.
    try:
        await basic_http_check(http_client)
    except Exception as e:
        logger.info("Server's http access failed")  # Program continues, waiting for the server to be active.

    # Todo: Token could be better got from the server as a result from some registration process
    my_token = input("Enter uid: ")
    if not my_token:
        my_token = uuid.uuid4()

    client_ops = ClientOps(my_token, http_client, logger)  # Init the client operations class

    input_queue = asyncio.Queue()  # Initiates the user keyboard input queue

    listen_to_user_event = asyncio.Event()  # The event will trigger listening to user inputs
    listen_to_user_event.set()  # Initially set the event so that we can get user input

    # Async use a separated thread, so the below plus the above input_thread allow the input thread to communicate
    # with the async one

    threading.Thread(target=input_thread, args=(input_queue, events_loop, listen_to_user_event, http_client),
                     daemon=True).start()

    # Create tasks and use gather on these tasks
    websocket_client = WebSocketClient()

    try:
        task1 = asyncio.create_task(
            websocket_client.websocket_listener(my_token, listen_to_user_event, http_client, client_ops))
        task2 = asyncio.create_task(
            user_input_handler(input_queue, listen_to_user_event, http_client, client_ops))
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
    async_events_loop = asyncio.get_event_loop()

    try:
        async_events_loop.run_until_complete(main(http_client, async_events_loop))
    except (KeyboardInterrupt, GracefulExit):  # When ctrl-c is pressed, SIGINT raises this exception.
        logger.info("Shutting down gracefully...")
        # http_client.stop()  # No need to close here, as closed by main.
    finally:
        logger.info("Shutting down gracefully. "
                    f"Closing http_client session: {http_client.session} and asyncio event loop...")
        async_events_loop.run_until_complete(http_client.close())
        async_events_loop.close()
