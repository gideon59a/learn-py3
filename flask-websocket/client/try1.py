from websocket import create_connection
#import ssl
ws = create_connection("ws://echo.websocket.org/")
                       #sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False, "ssl_version": ssl.PROTOCOL_TLSv1})
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
