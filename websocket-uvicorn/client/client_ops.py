

class ClientOps:

    def __init__(self, my_token, http_client, logger):
        self.my_token = my_token
        self.http_client = http_client
        self.logger = logger
        self.print_to_user = None

    def print_request_from_user(self):
        msg = "Please enter a command 'lp' 'sp' or 'g'  (or 'exit' to quit, or 'cont' to force continuing):"
        return msg

    async def process_user_input(self, data):
        cmd = data
        jdata = {
            "key": "cmd",
            "value": cmd}
        self.logger.info(f"CMD got: {cmd}")

        if cmd == "exit":
            self.http_client.stop()
            return {"status": "ok", "action": "to_exit"}

        response_json = None
        http_code = None
        result = {"status": "ok", "action": None, "response_json": None, "http_code": None}
        if 'l' in cmd:
            result["action"] = "to_clear_event"
        if 'p' in cmd:
            endpoint = '/my_endpoint4'
            response_json, http_code = await self.http_client.post(f'{endpoint}?ws_token={self.my_token}', json_data=jdata)
        elif 'z' in cmd:
            endpoint = '/play'
            response_json, http_code = await self.http_client.post(f'{endpoint}?ws_token={self.my_token}', json_data=jdata)
        elif 'g' in cmd:
            endpoint = '/my_endpoint3'
            response_json, http_code = await self.http_client.get(f'{endpoint}?ws_token={self.my_token}')
        else:
            pass
        result["response_json"] = response_json
        result["http_code"] = http_code
        self.logger.debug("AFTER HTTP")
        return result

    def process_server_message(self, data):
        self.logger.info(f"Processing ws message: {data}")
        status = "ok"
        self.logger.info(f"status: {status}")
        return {"status": "ok", "action": None}
