class ClientOps:

    def __init__(self, my_token, http_client):
        self.my_token = my_token
        self.http_client = http_client

    async def process_user_input(self, data):
        cmd = data
        print(f"CMD got: {cmd}")

        if cmd == "exit":
            self.http_client.stop()
            return {"status": "ok", "action": "to_exit"}

        result = {"status": "ok", "action": None}
        if 'l' in cmd:
            result["action"] = "to_clear_event"
        if 'p' in cmd:
            endpoint = '/my_endpoint4'
            data = {
                "key": "cmd",
                "value": cmd}
            await self.http_client.post(f'{endpoint}?ws_token={self.my_token}', json_data=data)
        elif 'g' in cmd:
            endpoint = '/my_endpoint3'
            await self.http_client.get(f'{endpoint}?ws_token={self.my_token}')
        else:
            pass
        print("AFTER HTTP")
        return result

    def process_server_message(self, data):
        print(f"Processing ws message: {data}")
        status = "ok"
        print(f"status: {status}")
        return {"status": "ok", "action": None}
