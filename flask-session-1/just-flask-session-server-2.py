# Ref: https://www.askpython.com/python-modules/flask/flask-sessions
# Note: The "session" is a dictionary that contains data that exists throughout the session. Any key can be stored, i.e.
# not just "Username" that is shown below.
# my-sid: Note that my_sid here is a random name chosen, not related to socketio's request.sid !!!

from flask import Flask, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "xyz"

@app.route('/old-setsession')
def oldsetsession():
    session['Username'] = 'Admin'
    session['Username'] = 'Admin'
    msg = f"The session has been Set"
    print(f'On /old-setsession return {msg}')
    return f"The session has been Set"  # The return data appears also in a web page

@app.route('/setsession')
def setsession():
    random.randint(1,1000)
    session['Username'] = 'Admin'
    session['my_sid'] = random.randint(1, 1000)
    print(f' on /setsession return {session["Username"]} {session["my_sid"]}')
    #print(f'local session id: {id(session)}')
    return f"The session has been Set with username and my_sid: {session['Username']} {session['my_sid']}"  # The return data appears also in a web page


@app.route('/getsession')
def getsession():
    if 'Username' in session:
        username = session['Username']
        #my_sid = session['my_sid'] if 'my_sid' in session.keys() else ""
        if 'my_sid' in session.keys():
            my_sid = session['my_sid']
        else:
            my_sid = ""
        print(f'On /getsession return "Welcome {username} having my_sid {my_sid}')
        #print(f'local session id: {id(session)}')
        return f"Welcome {username} having my_sid {my_sid}"
    else:
        print(f'On /getsession return Welcome Anonymous')
        #print(f'local session id: {id(session)}')
        return "Welcome Anonymous"

@app.route('/getsession-json')
def getsession_json():
    if 'Username' in session:  # The server has a specific session object per client session
        username = session['Username']
        if 'my_sid' in session.keys():
            my_sid = session['my_sid']
        else:
            my_sid = ""
        msg = {"Welcome": username, "my_sid": my_sid}
        print(f'on /getsession-json print {msg}')
        #print(f'local session id: {id(session)}')
        print(f'on /getsession-json print session dict: {session.__dict__}')
        return jsonify(msg)
    else:
        print(f'on /getsession-json print {"Welcome": Anonymous, "my_sid": my_sid}')
        return jsonify({"Welcome": "Anonymous", "my_sid": ""})


@app.route('/popsession')
def popsession():
    session.pop('Username', None)
    print(f'on /popsession return "Session Deleted"')
    return "Session Deleted"


app.run(host='0.0.0.0', port=5000)