from flask import Flask, render_template
from flask_socketio import SocketIO
from Tetris import Tetris
from telemetry import Telemetry
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connected')
def on_connect(json):
    print('connected: ' + str(json))
    Telemetry.bind_socket(socketio)
    def worker():
        print('thread')
        tetris = Tetris()
        tetris.begin()
    t = threading.Thread(target=worker)
    t.start()

@socketio.on('action')
def on_action(json):
    print('action: ' + str(json))

@socketio.on('end_action')
def on_end_action(json):
    print('action end: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)
