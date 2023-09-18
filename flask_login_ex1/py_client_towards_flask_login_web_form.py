# NOTE: The below doesn't use session, and therefore the login doesn't remain.

import json

from commons.logger import Alogger
from commons.http_requests import HttpRequests

my_logger = Alogger('test.log')
logger = my_logger.get_logger()

URL_PREFIX = "http://192.168.1.211:5000/"
req = HttpRequests(logger)

logger.debug(f'Check is server is alive:')

url1 =  "http://192.168.1.211:5000/logmein-py"
payload = {"username": "gideon1"}
code, rjson = req.post(url1, payload)
logger.info(f' json got: {type(rjson)} , {rjson} code: {code}')

url2 =  "http://192.168.1.211:5000/home"
code, rjson = req.get(url2)
logger.info(f' json got: {type(rjson)} , {rjson} code: {code}')


