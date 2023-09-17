Ex#1: flask-session-server-1.py with the 3 files at the ./templates folder, tested with chrome

Ex#2: just-flask-session-server-2.py, tested with chrome

Ex#2B: just-flask-session-server-2.py, tested with a python requests client named just-flask-session-client-2
(!!) tests:
 - session with sid information sent to the client only for its own session information.

Notes:
a client
- creates a session with the server, by s = requests.Session()
- accesses server e.g. at /setsession
the server (that supports flask session)
- can set a value in session[“some key”]. This session dict is unique per each client session!
- The server may send this info back to the client.
