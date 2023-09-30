import asyncio
import time

start_time = time.time()


class ServerOps:
    def __init__(self, logger):
        self.logger = logger
        self.connected_clients = []
        self.game_status = 0
        self.players = []

    def update_connected_clients(self, connected_clients):
        self.connected_clients = connected_clients

    async def send_ws_to_clients(self, unicast=False, ws_token=None, message=None):
        """
        :param unicast: If True send only to the client with the ws_token. Otherwise, send to all clients.
        :param ws_token:
        :param message:
        :return:
        """
        sent = False
        for client in self.connected_clients:
            if unicast:
                self.logger.info("Send a message to the WebSocket that initiated the request")
                if client.scope.get("query_string") == f"token={ws_token}".encode():
                    if not message:
                        message = f"Task triggered by you is done! Time: {time.time() - start_time}"
                    self.logger.info(f"Unicast message for {ws_token}: {message}")
                    await client.send_text(message)
                    sent = True
            else:
                client_token = client.scope.get("query_string")
                if not message:
                    message = f"Task result broadcast: {message}"
                self.logger.info(f"Broadcast message for {client_token}: {message}")
                await client.send_text(message)
                sent = True
        return sent

    async def do_my_stuff(self, ws_token: str):
        self.logger.info(f"Processing user request - waiting for 2 seconds\n...........")
        await asyncio.sleep(2)  # Simulating a long-running task
        sent = await self.send_ws_to_clients(unicast=True, ws_token=ws_token)
        self.logger.info(f"Sent: {sent}")


    async def play(self, ws_token, data=None):
        self.logger.info(f"ZZZZZZZZZZ for ws_token: {ws_token}")
        return
        if ws_token not in self.players:
            self.players.append(ws_token)
            if len(self.players) == 2:
                self.game_status = 1
                await self.send_ws_to_clients(message=f"play done. Status: {self.game_status}")
                return
            else:
                msg = "Wait for the other player to join"
        else:
            msg = "You have already registered. Wait for the other player to join"
        await self.send_ws_to_clients(unicast=True, ws_token=ws_token, message=msg)



