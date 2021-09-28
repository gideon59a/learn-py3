# Ref: https://www.askpython.com/python-modules/flask/flask-sessions
# Note: The "session" is a dictionary that contains data that exists throughout the session. Any key can be stored, i.e.
# not just "Username" that is shown below.
# SID Note that sid here is a random name chosen, not related to socketio's request.sid !!!

from flask import Flask, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "xyz"

@app.route('/old-setsession')
def oldsetsession():
    session['Username'] = 'Admin'
    return f"The session has been Set"  # The return data appears also in a web page

@app.route('/setsession')
def setsession():
    random.randint(1,1000)
    session['Username'] = 'Admin'
    session['sid'] = random.randint(1,1000)
    return f"The session has been Set with username and sid: {session['Username']} {session['sid']}"  # The return data appears also in a web page


@app.route('/getsession')
def getsession():
    if 'Username' in session:
        username = session['Username']
        #sid = session['sid'] if 'sid' in session.keys() else ""
        if 'sid' in session.keys():
            sid = session['sid']
        else:
            sid = ""
        return f"Welcome {username} having sid {sid}"
    else:
        return "Welcome Anonymous"

@app.route('/getsession-json')
def getsession_json():
    if 'Username' in session:
        username = session['Username']
        if 'sid' in session.keys():
            sid = session['sid']
        else:
            sid = ""
        return jsonify({"Welcome": username, "sid": sid})
    else:
        return jsonify({"Welcome": "Anonymous", "sid": ""})


@app.route('/popsession')
def popsession():
    session.pop('Username', None)
    return "Session Deleted"


app.run(host='0.0.0.0', port=5000)