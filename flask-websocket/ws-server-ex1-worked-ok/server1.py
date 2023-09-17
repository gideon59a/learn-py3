# Ref (works ok): https://pythonprogramminglanguage.com/python-flask-websocket/
# NOTE: The server fails until I downgraded flask-socketio to 4.3.2 per https://github.com/miguelgrinberg/Flask-SocketIO/issues/1432
# C:\Python\Python39\Scripts\pip.exe install -Iv flask-socketio==4.3.2

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('after connect', {'data': 'Lets dance'})
    #emit('after connect', {'data': 'sent again'})
    #emit('after connect', {'data': '3rd time'})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")

