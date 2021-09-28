# Ref: https://flask-socketio.readthedocs.io/en/latest/getting_started.html#initialization

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
#socketio = SocketIO(app, logger=False, engineio_logger=False, policy_server=False, manage_session=False,
#                    cors_allowed_origins=["http://127.0.0.1"])  #, message_queue=socket_io_msg_q)

@app.route('/')
def index():
    print("Within index")
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print("Within test_connect")
    emit('after connect', {'data': 'server2 app connected...'})

@socketio.on('message')
def handle_message(data):
    print("Within handle_message")
    print('received message: ' + data)

if __name__ == '__main__':
    socketio.run(app,  port=5001, debug=True)
