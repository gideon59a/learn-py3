import requests
import json

class HttpRequests():

    def __init__(self, logger):
        self.logger = logger
        self.timeout = 1.5

    def get(self, url):
        status_code = 400
        rjson = {}
        try:
            self.logger.debug(f'GET url = {url} ')
            response = requests.get(url, timeout=self.timeout)
            status_code = response.status_code
            if status_code > 210:
                self.logger.error("request failure")
            self.logger.debug(f'Get response,json: {type(response.json())} , {response.json()}')
            rjson = json.loads(response.json().replace("\'", "\""))  # json requires " rather than '
            # tech note: An alternative to the above using json could be:
            # import ast
            # rjson=ast.literal_eval(response.json())
            #XX self.logger.debug(f'*** http AFTER json.load')
        except Exception as e:
            self.logger.warn(f'http GET request exception: {str(e)}')
        return status_code, rjson

    def delete(self, url):
        status_code = 0
        rjson = {}
        try:
            self.logger.debug(f'Delete method {url}')
            response = requests.delete(url, timeout=self.timeout)
            status_code = response.status_code
            if status_code > 210:
                self.logger.error(f'Delete request failure. url: {url} status_code: {status_code}')
            self.logger.debug(f'Delete response,json: {type(response.json())} , {response.json()}')
            rjson = json.loads(response.json())
        except Exception as e:
            self.logger.warn(f'http DELETE request exception: {str(e)}')
        return status_code, rjson

    def post(self, url, payload):
        status_code = 0
        rjson = {}
        #self.logger.debug(f'===== {type(payload)}  {url} {payload}')
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            status_code = response.status_code
            if status_code > 210:
                self.logger.error(f'Post request failure. url: {url} status_code: {status_code}')
            self.logger.debug(f'Post response,json: {type(response.json())} , {response.json()}')
            rjson = response.json()
        except Exception as e:
            self.logger.warn(f'http POST request exception: {str(e)}')
        return status_code, rjson
