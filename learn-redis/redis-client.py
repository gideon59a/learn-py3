# Ref #1: https://realpython.com/python-redis/
# At the remote server 10.5.224.10:
#    # docker run --name learn-redis -p 36379:6379 -d redis
#    # iptables -I INPUT -p tcp -m tcp --dport 36379 -j ACCEPT
# At some client location
#    # python3 -m pip install redis
#    # python3
#    >>> import redis

import redis

r1 = redis.Redis(host='10.5.224.10', port=36379, db=1, password=None)
r1.mset({"Croatia1": "Zagreb1", "Bahamas1": "Nassau1"})
key1 = r1.get("Croatia1")
print(key1)
